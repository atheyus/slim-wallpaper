#!/usr/bin/env python2


import pygtk
pygtk.require('2.0')
import gtk
import re
import os.path

configuracion = "/etc/slim.conf"

def tema(t):
    theme = open(t)
    for linea in theme:
        if re.search("current_theme.*",linea):
            tema = linea.split()
            return tema[1]
        else:
            pass

tema = tema(configuracion)

imagen = "/usr/share/slim/themes/%s/background" %(tema)

if os.path.exists(imagen + '.png'):
    imagen = imagen + '.png'; e = 'png'
elif os.path.exists(imagen + '.jpeg'):
    imagen = imagen + '.jpeg'; e = 'jpeg'
else:
    os.path.exists(imagen + '.jpg')
    imagen = imagen + '.jpg'; e = 'jpg'

path = "/usr/share/slim/themes/%s/background.%s" %(tema,e)
nueva_imagen = ''

class Fondo():
    def __init__(self):
        self.ventana = gtk.Window(gtk.WINDOW_TOPLEVEL)
        self.ventana.set_position(gtk.WIN_POS_CENTER)
        self.ventana.set_default_size(300, 200)
        self.ventana.set_title('Slim Wallpaper')
        self.ventana.connect("destroy", self.salir)
        self.ventana.set_resizable(False)
        self.im = gtk.Image()
        self.vbox = gtk.VBox(gtk.FALSE,0)
        self.hbox = gtk.HBox(gtk.FALSE,0)
        self.label = gtk.Label("Imagen: ")
        self.separador0 = gtk.HSeparator()
        self.separador1 = gtk.HSeparator()
        self.bsalir = gtk.Button(stock=gtk.STOCK_CLOSE)
        self.bimagen = gtk.Button(label="Selccionar Imagen Nueva")
        self.aceptar = gtk.Button(stock=gtk.STOCK_APPLY)
        self.Imagen =gtk.Button(stock=gtk.STOCK_DELETE)
        self.colocar_imagen(imagen)
        self.bsalir.connect('clicked', self.salir)
        self.aceptar.connect('clicked', self.aplicar)
        self.bimagen.connect('clicked', self.abrir)
        self.hbox.pack_start(self.aceptar,gtk.FALSE,gtk.FALSE,10)
        self.hbox.pack_start(self.bimagen,gtk.FALSE,gtk.FALSE,10)
        self.hbox.pack_start(self.bsalir,gtk.FALSE,gtk.FALSE,10)
        self.vbox.pack_start(self.label,gtk.FALSE,gtk.FALSE,2)
        self.vbox.pack_start(self.separador0,gtk.FALSE,gtk.FALSE,2)
        self.vbox.pack_start(self.im,gtk.FALSE,gtk.FALSE,4)
        self.vbox.pack_start(self.separador1,gtk.FALSE,gtk.FALSE,0)
        self.vbox.pack_start(self.hbox,gtk.FALSE,gtk.FALSE,0)
        self.ventana.add(self.vbox)
        self.ventana.show_all()
    def abrir(self,action):
        dialogo = gtk.FileChooserDialog("Selecciona una imagen:",
                                  self.ventana,
                                  gtk.FILE_CHOOSER_ACTION_OPEN,
                                  (gtk.STOCK_CANCEL, gtk.RESPONSE_CANCEL,
                                  gtk.STOCK_OPEN, gtk.RESPONSE_OK))
        dialogo.set_default_response(gtk.RESPONSE_OK)
        respuesta = dialogo.run()
        if respuesta == gtk.RESPONSE_OK:
            global imagen
            imagen = dialogo.get_filename()
            self.colocar_imagen(imagen)
        dialogo.destroy()

    def colocar_imagen(self,imagen):
        error = None
        try:
            self.pixbuf = gtk.gdk.pixbuf_new_from_file(imagen)
            self.scaled_buf = self.pixbuf.scale_simple(230,180,gtk.gdk.INTERP_BILINEAR)
            self.im.set_from_pixbuf(self.scaled_buf)
        except:
            error = gtk.MessageDialog(self.ventana,
                                         gtk.DIALOG_DESTROY_WITH_PARENT,
                                         gtk.MESSAGE_ERROR,
                                         gtk.BUTTONS_CLOSE,
                                         "Error no se puede colocar %s:" %
                                         (imagen))
        if error is not None:
            error.connect("response", lambda w,resp: w.destroy())
            error.show()
    def aplicar(self,widget,data = None):
        orden = 'pkexec cp %s %s' %(imagen,path)
        os.system(orden)
    def salir(self,widget,data = None):
        gtk.main_quit()
    def main(self):
        gtk.main()

if __name__ == "__main__":
    background = Fondo()
    background.main()
