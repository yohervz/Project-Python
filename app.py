import os
import sqlite3
import tkinter
import tkinter.ttk
from tkinter import messagebox

#Esta funcion crea la base de datos en caso de que no exista
def crearBaseDeDatos(db):
	ejecucion = True
	try:
		baseDeDatos = sqlite3.connect(db)
		cursor = baseDeDatos.cursor()
		cursor.execute(""" create table if not exists clientes(
			nombre varchar(20),
			apellido varchar(20),
			correo varchar(255),
			telefono integer,
			nacionalidad text)""")
	except:
		ejecucion = False
	finally:
		baseDeDatos.commit()
		baseDeDatos.close()

	return ejecucion


#Esta función inserta datos en la base de datos
def insertarDatos(db, datos):
	ejecucion = True
	try:
		baseDeDatos = sqlite3.connect(db)
		cursor = baseDeDatos.cursor()

		#Se busca si hay un correo repetido
		coincidencias = cursor.execute(f"select correo from clientes where correo = '{datos[2]}'")
		coincidencias = coincidencias.fetchall()

		#En caso de que el correo este repetido no se agrega a la base de datos
		if len(coincidencias)  > 0:
			ejecucion = False
		#Si es unico se agrega la información
		else:
			cursor.execute("insert into clientes values (?,?,?,?,?)", datos)
	except Exception as e:
		ejecucion = False
	finally:
		baseDeDatos.commit()
		baseDeDatos.close()

	return ejecucion

#Esta función se encarga de buscar datos en la base de datos
def buscarDato(db, campo, datoBuscado):
	#En caso de que no se encuenter coincidencias se retornara un array vacio
	resultado = []
	try:
		baseDeDatos = sqlite3.connect(db)
		cursor = baseDeDatos.cursor()
		cursor.execute(f"select * from clientes where {campo} = '{datoBuscado}'")
		resultado = cursor.fetchall()
	except Exception as e:
		ejecucion = False
		
	finally:
		baseDeDatos.commit()
		baseDeDatos.close()

	return resultado

#Esta función elimina clientes de la base de datos
def eliminarCliente(db, dato):
	ejecucion = True
	try:
		baseDeDatos = sqlite3.connect(db)
		cursor = baseDeDatos.cursor()
		cursor.execute(f"delete from clientes where correo = '{dato}'")
	except:
		ejecucion = False
	finally:
		baseDeDatos.commit()
		baseDeDatos.close()

	return ejecucion

#Esta función actualiza información en la base de datos
def actualizarCliente(db, datos, correo):
	ejecucion = True
	try:
		baseDeDatos = sqlite3.connect(db)
		cursor = baseDeDatos.cursor()
		cursor.execute(f"replace into clientes values (?,?,?,?,?) where correo = '{correo}'", datos)

	except Exception as e:
		ejecucion = False
	
	finally:
		baseDeDatos.commit()
		baseDeDatos.close()

#Clase para gestionar la base de datos
class Aplicacion:
	
	def __init__(self):
		"""Esta función se ejecuta automaticamente al crear el objeto"""

		#Objeto principal de la GUI
		self.ventanaPrincipal = tkinter.Tk()

		self.ventanaPrincipal.title("Administrador de clientes")

		#Dimensiones de la ventana
		self.ventanaPrincipal.geometry("500x120")

		#Titulo superior de la ventana
		self.titulo = tkinter.Label(self.ventanaPrincipal, text="Ingrese el correo",font=("", 15))

		#Caja para buscar usuarios
		self.entradaDeBusqueda = tkinter.Entry(self.ventanaPrincipal, width=40)

		#Boton de buscar
		self.botonDeBuscar = tkinter.Button(self.ventanaPrincipal, text="Buscar", command=self.buscarCliente)

		#Menu de opciones
		self.menuOpciones = tkinter.Menu(self.ventanaPrincipal)
		self.menuOpcionUsuarios = tkinter.Menu(self.menuOpciones, tearoff=0)
		self.menuOpcionUsuarios.add_command(label="Agregar", command=self.lanzarVentanaParaAgregarUsuarios)
		self.menuEditar = tkinter.Menu(self.menuOpciones, tearoff=0)
		self.menuOpciones.add_cascade(label="Usuarios", menu=self.menuOpcionUsuarios)
		
		#Esta variable gestiona si hay ventanas secundarias para agregar
		self.ventanaSecundaria = False
		pass

	def configurarAplicacion(self):
		"""	Esta función posiciona los elementos """

		#Se agrega el menu a la ventana
		self.ventanaPrincipal.config(menu=self.menuOpciones)
		self.titulo.pack()
		#Cuando se precione la tecla Enter iniciaria la función agregarElementosALista
		self.entradaDeBusqueda.bind("<Return>", self.buscarCliente)
		self.entradaDeBusqueda.pack()
		self.botonDeBuscar.pack()

		pass

	def lanzarAplicacion(self):
		"""Esta función pone a correr la aplicación"""
		self.configurarAplicacion()
		#Esto se encarga de poner en focus la caja de busqueda
		self.entradaDeBusqueda.focus()
		#Este bucle gestiona la ejecución del programa
		self.ventanaPrincipal.mainloop()
		pass

	def lanzarVentanaDeBusqueda(self, datos):
		"""Esta función crea una ventana con la información buscada"""

		#Raiz de la ventana
		self.ventanaBusqueda = tkinter.Toplevel()
		#Este es el correo que se buscó anterioremente
		self.ultimaBusqueda = datos[0][2]
		self.ventanaBusqueda.geometry("300x150")

		#Se obtienen el nombre y apellido y se muestran en el titulo
		self.ventanaBusqueda.title(datos[0][0] + " " + datos[0][1])


		#Se imprimen los datos devueltos por la base de datos
		nombre = tkinter.Label(self.ventanaBusqueda, text=f"{datos[0][0]} {datos[0][1]}")
		nombre.pack()

		correo = tkinter.Label(self.ventanaBusqueda, text=f"{datos[0][2]}")
		correo.pack()

		telefono = tkinter.Label(self.ventanaBusqueda, text=f"{datos[0][3]}")
		telefono.pack()

		localidad = tkinter.Label(self.ventanaBusqueda, text=f"{datos[0][4]}")
		localidad.pack()

		#Este boton llama a una función para eliminar base de datos
		botonEliminiarCliente = tkinter.Button(self.ventanaBusqueda, text="Eliminar", command=self.eliminarCliente)
		botonEliminiarCliente.pack()
		#Este botonllama a una función para rditar la base de datos
		botonEditarCliente = tkinter.Button(self.ventanaBusqueda, text="Editar", command=self.lanzarVentanaParaEditarUsuarios)
		botonEditarCliente.pack()

		#Inicia la aplicación
		self.ventanaBusqueda.mainloop()
		pass

	def buscarCliente(self, event=None):
		"""Esta función busca un cliente y lo muestra por una ventana secundaria"""
		datoBuscar = self.entradaDeBusqueda.get()
		resultado = buscarDato("baseDeDatos.db", "correo", str(datoBuscar))
		if len(resultado) > 0:
			self.lanzarVentanaDeBusqueda(resultado)
		pass

	def agregarCliente(self):
		"""Esta función agrega usuarios a la base de datos"""

		#Información de los campos de la ventana de agregar usuarios 
		datos = (self.entradaDeNombre.get(),self.entradaDeApellido.get(), self.entradaDeCorreo.get(), self.entradaDeTelefono.get(), self.entradaDeLocalidad.get())
		camposVacios = False
		
		#Verifica si todos los campos estan ocupados
		for dato in datos:
			if len(dato) == 0:
				camposVacios = True

		#Si los campos están vacios muestra un mensaje
		if camposVacios == True:
			messagebox.showinfo(message="Debe rellenar todos los campos", title="Campos incompletos")
		#Si todos esta rellenos envia los datos para ser guardados
		else:
			if insertarDatos("baseDeDatos.db", datos) == False:
				messagebox.showinfo(message="Este correo está registrado a otro usuario", title="Correo repetido")
			else:
				self.ventanaUsuarios.destroy()
				messagebox.showinfo(message="Registro completado", title="Exito")

	def actualizarCliente(self):
		"""Esta función actualiza los usuarios"""

		#Información de los campos de la ventana de actualizar usuarios 
		datos = (self.entradaDeNombreEditar.get(),self.entradaDeApellidoEditar.get(), self.entradaDeCorreoEditar.get(), self.entradaDeTelefonoEditar.get(), self.entradaDeLocalidadEditar.get())
		camposVacios = False
		
		#Verifica que todos los datos estan lleno
		for dato in datos:
			if len(dato) == 0:
				camposVacios = True

		#Si los campos están vacios muestra un mensaje
		if camposVacios == True:
			messagebox.showinfo(message="Debe rellenar todos los campos", title="Campos incompletos")
		#Si todos esta rellenos envia los datos para ser guardados
		else:
			if actualizarCliente("baseDeDatos.db", datos, self.ultimaBusqueda) == False:
				messagebox.showinfo(message="Este correo está registrado a otro usuario", title="Correo repetido")
			else:
				self.ventanaUsuariosEditar.destroy()
				messagebox.showinfo(message="Actualizacion completada", title="Exito")
		
	def eliminarCliente(self):
		"""Esta función elimina clientes de la base de usuarios"""

		if eliminarCliente("baseDeDatos.db", self.ultimaBusqueda) == False:
			messagebox.showinfo(message="Ha ocurrido un error", title="Error")
		else:
			self.ventanaBusqueda.destroy()
			messagebox.showinfo(message="Proceso terminado", title="Usuario borrado")
		pass

	def crearVentanaParaAgregarDatos(self):
		"""Esta función crea la ventana para agregar usuarios"""
		self.ventanaUsuarios = tkinter.Toplevel()
		self.ventanaUsuarios.geometry("300x250")
		self.ventanaUsuarios.title("Agregar Usuarios")
		self.textoNombre = tkinter.Label(self.ventanaUsuarios, text="Nombre")
		self.entradaDeNombre = tkinter.Entry(self.ventanaUsuarios)
		self.textoApellido = tkinter.Label(self.ventanaUsuarios, text="Apellido")
		self.entradaDeApellido = tkinter.Entry(self.ventanaUsuarios)
		self.textoCorreo = tkinter.Label(self.ventanaUsuarios, text="Correo")
		self.entradaDeCorreo = tkinter.Entry(self.ventanaUsuarios, width=30)
		self.textoTelefono = tkinter.Label(self.ventanaUsuarios, text="Telefono")
		self.entradaDeTelefono = tkinter.Entry(self.ventanaUsuarios)
		self.textoLocalidad = tkinter.Label(self.ventanaUsuarios, text="Localidad")
		self.entradaDeLocalidad = tkinter.Entry(self.ventanaUsuarios)
		self.botonAgregarUsuario = tkinter.Button(self.ventanaUsuarios, text="Agregar", command=self.agregarCliente)
		pass

	def configurarVentanaParaAgregarUsuarios(self):
		"""Esta función configura la ventana de agregar usuarios"""
		self.textoNombre.pack()
		self.entradaDeNombre.pack()
		self.textoApellido.pack()
		self.entradaDeApellido.pack()
		self.textoCorreo.pack()
		self.entradaDeCorreo.pack()
		self.textoTelefono.pack()
		self.entradaDeTelefono.pack()
		self.textoLocalidad.pack()
		self.entradaDeLocalidad.pack()
		self.botonAgregarUsuario.pack()
		pass

	def lanzarVentanaParaAgregarUsuarios(self):
		"""Lanza la ventana de agregar usuarios"""
		self.crearVentanaParaAgregarDatos()
		self.configurarVentanaParaAgregarUsuarios()
		self.entradaDeNombre.focus()
		self.ventanaUsuarios.mainloop()

	def crearVentanaParaEditarUsuarios(self):
		"""Esta función crea la ventana para editar usuarios"""
		self.ventanaUsuariosEditar = tkinter.Toplevel()
		self.ventanaUsuariosEditar.geometry("300x300")
		self.ventanaUsuariosEditar.title("Agregar Usuarios")
		self.textoNombreEditar = tkinter.Label(self.ventanaUsuariosEditar, text="Nombre")
		self.entradaDeNombreEditar = tkinter.Entry(self.ventanaUsuariosEditar)
		self.textoApellidoEditar = tkinter.Label(self.ventanaUsuariosEditar, text="Apellido")
		self.entradaDeApellidoEditar = tkinter.Entry(self.ventanaUsuariosEditar)
		self.textoCorreoEditar = tkinter.Label(self.ventanaUsuariosEditar, text="Correo")
		self.entradaDeCorreoEditar = tkinter.Entry(self.ventanaUsuariosEditar, width=30)
		self.textoTelefonoEditar = tkinter.Label(self.ventanaUsuariosEditar, text="Telefono")
		self.entradaDeTelefonoEditar = tkinter.Entry(self.ventanaUsuariosEditar)
		self.textoLocalidadEditar = tkinter.Label(self.ventanaUsuariosEditar, text="Localidad")
		self.entradaDeLocalidadEditar = tkinter.Entry(self.ventanaUsuariosEditar)
		self.botonDeActualizarUsuario = tkinter.Button(self.ventanaUsuariosEditar, text="Actualizar", command=self.actualizarCliente)
		pass

	def configurarVentanaParaEditarUsuarios(self):
		"""Esta función configura la ventana de agregar usuarios"""
		self.textoNombreEditar.pack()
		self.entradaDeNombreEditar.pack()
		self.textoApellidoEditar.pack()
		self.entradaDeApellidoEditar.pack()
		self.textoCorreoEditar.pack()
		self.entradaDeCorreoEditar.pack()
		self.entradaDeCorreoEditar.insert(0, self.ultimaBusqueda)
		self.textoTelefonoEditar.pack()
		self.entradaDeTelefonoEditar.pack()
		self.textoLocalidadEditar.pack()
		self.entradaDeLocalidadEditar.pack()
		self.botonDeActualizarUsuario.pack()
		pass

	def lanzarVentanaParaEditarUsuarios(self):
		"""Lanza la ventana de agregar usuarios"""
		self.ventanaBusqueda.destroy()
		self.crearVentanaParaEditarUsuarios()
		self.configurarVentanaParaEditarUsuarios()
		self.entradaDeNombreEditar.focus()
		self.ventanaUsuariosEditar.mainloop()

#Si la base de datos no existe es creada
if crearBaseDeDatos("baseDeDatos.db") == False:
	#Si lanza error se cierra el programa
	exit()

app = Aplicacion()
app.lanzarAplicacion()