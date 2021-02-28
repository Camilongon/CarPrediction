import cloudpickle
from flask import Flask, render_template, flash, url_for, redirect, request
from flask_wtf import FlaskForm
from wtforms import SubmitField, DateField, DecimalField, IntegerField, SelectField
from wtforms.validators import DataRequired, NumberRange
import pandas as pd

app = Flask(__name__)
app.config['SECRET_KEY'] = 'proyecto1'

model = cloudpickle.load(open('model_carpre_vb.pkl', 'rb'))

class Cuestionario(FlaskForm):
    marcas=['Opel', 'Daewoo', 'Ambassador', 'Ashok', 'Datsun', 'Fiat', 'Force',
       'Nissan', 'Maruti', 'Renault', 'Chevrolet', 'Volkswagen', 'Tata',
       'Mahindra', 'MG', 'Kia', 'Isuzu', 'Hyundai', 'Mitsubishi', 'Honda',
       'Volvo', 'Ford', 'Skoda', 'Jaguar', 'Toyota', 'Jeep', 'Land', 'Lexus',
       'Mercedes-Benz', 'Audi', 'BMW']
    
    fuel_cat = ['Diesel', 'Petrol', 'LPG', 'CNG']
    transmission_cat = ['Manual', 'Automatic']
    seller_cat = ['Individual', 'Dealer', 'Trustmark Dealer']
    owner_cat = ['First Owner', 'Second Owner', 'Third Owner', 'Fourth & Above Owner', 'Test Drive Car']
    
    marca =SelectField('Marca de Automovil', choices=marcas)
    fuel = SelectField('Tipo de Combustible', choices=fuel_cat)
    seller_type = SelectField('Tipe de Vendedor', choices=seller_cat)
    transmission = SelectField('Transmision', choices=transmission_cat)
    owner = SelectField('Dueño', choices=owner_cat)
   
    seats= IntegerField('Número de asientos', validators=[DataRequired(), NumberRange(min=1, max=8, message='Cantidad invalida de asientos permitada')])
    
    year = IntegerField('Año del auto', validators=[DataRequired(), NumberRange(min=1960, max=2021, message='Ingresar valor no mayor a 2021')])
    
    
    km_driven=DecimalField('Kilómetros conducidos', validators=[DataRequired()])
    mileage=DecimalField('Kilometraje (Mileage)',validators=[DataRequired()] )
    max_power=DecimalField('Break Horse Power (max_power)', validators=[DataRequired()])
    
    submit=SubmitField('Submit')
    
    
@app.route('/')
@app.route('/home', methods=['GET'])
def base():
    return render_template('base.html')

@app.route('/predict', methods=['GET', 'POST'])
def predict():
    form = Cuestionario()
    if request.method == "POST":
        
        marca = form.marca.data
        fuel = form.fuel.data
        seller = form.seller_type.data
        trans = form.transmission.data
        ow = form.owner.data
        seats = form.seats.data
        year = int(2021-form.year.data)
        km = form.km_driven.data
        mil = form.mileage.data
        maxp = form.max_power.data
        
        
        val = [ marca, fuel, seller, trans, ow, seats, year, km, mil, maxp]
        col = ['marca','fuel','seller_type','transmission','owner','seats','num_year','km_driven','mileage','max_power']
        
        df_pred = pd.DataFrame(val).T
        df_pred.columns = col
        
        prediction = model.predict(df_pred)
        flash("Precio sugerido: {0}".format(prediction[0]), 'success')
        #else:
        #    flash("Valores incorrectos", 'warning')
        return redirect(url_for('base'))
    else:
        return render_template('prediction.html', form=form)
                           

if __name__ == '__main__':
    app.run(debug=True)