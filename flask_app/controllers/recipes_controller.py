from flask import render_template, redirect, session, request
from flask_app import app

#importa de los modelos
from flask_app.models.users import User
from flask_app.models.recipes import Recipe

@app.route('/new/recipe')
def new_recipe():
    if 'user_id' not in session:
        return redirect('/')

    #Yo sé que en sesión tengo el id de mi usuario (session['user_id'])
    #Queremos una función que en base a ese id me regrese una instancia del usuario
    formulario = {"id": session['user_id']}

    user = User.get_by_id(formulario)

    return render_template('new_recipes.html', user=user)

@app.route('/create/recipe', methods=['POST'])
def create_recipe():
    if 'user_id' not in session:
        return redirect('/')

    #validacion de receta
    if not Recipe.valida_receta(request.form):
        return redirect('/new/recipe')

    #guardamos receta
    Recipe.save(request.form)

    return redirect('/dashboard')

@app.route('/edit/recipe/<int:id>')
def edit_recipe(id):
    if 'user_id' not in session: #comprobamos q hay inicio de sesion
        return redirect('/')

    #Yo sé que en sesión tengo el id de mi usuario (session['user_id']) pero no se el nombre
    #Queremos una función que en base a ese id me regrese una instancia del usuario
    formulario = {"id": session['user_id']}

    user = User.get_by_id(formulario) #recibo la instancia de usuario en base a su id

#la instancia de la receta q se debe desplegar en editar en base al id q recibimos en url
    formulario_receta ={"id":id}
    r123 = Recipe.get_by_id(formulario_receta)
    return render_template('edit_recipe.html', user=user, recipe=r123)


@app.route('/update/recipe', methods=['POST'])
def update_recipe():
    #Verificar que haya iniciado sesion
    if 'user_id' not in session: #Comprobamos que inicia sesión
        return redirect('/')

    #recibimos formulario = request.form 
    #request.form = {name: "Albondigas", description:"123"....... recipe_id:1}

    #Verificar que todos los datos esten correctos
    if not Recipe.valida_receta(request.form):
        return redirect('/edit/recipe/'+request.form['recipe_id']) #/edit/recipe/1

    #Guardar los cambios
    Recipe.update(request.form)

    #Redireccionar a /dashboard
    return redirect('/dashboard')

@app.route('/delete/recipe/<int:id>')
def delete_recipe(id):
    #verificar q se haya iniciado sesssion
    if 'user_id' not in session: #Comprobamos que inicia sesión
        return redirect('/')

    #Borramos
    formulario = {"id": id}
    Recipe.delete(formulario)

    #redigirimos a /dashboard
    return redirect ('/dashboard')

@app.route('/view/recipe/<int:id>')
def view_recipe(id):
    #verificar q el usuario haya iniciado sesion
    if 'user_id' not in session: #Comprobamos que inicia sesión
        return redirect('/')

    #saber cual es el nombre del usuario q incio sesion
        #Yo sé que en sesión tengo el id de mi usuario (session['user_id']) pero no se el nombre
    #Queremos una función que en base a ese id me regrese una instancia del usuario
    formulario = {"id": session['user_id']}

    user = User.get_by_id(formulario) #recibo la instancia de usuario en base a su id


    #objeto receta q queremos desplegar
    formulario_receta = {"id":id}
    reciperr = Recipe.get_by_id(formulario_receta)
    #renderizar show_recipe.html
    return render_template('show_recipes.html', user=user , recipe=reciperr)
