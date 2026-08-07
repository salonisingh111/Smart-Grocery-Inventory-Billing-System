from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SelectField, FloatField, IntegerField, TextAreaField, DateField, FileField
from wtforms.validators import DataRequired, Email, Length, Optional, NumberRange

class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=3, max=50)])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember Me')

class SensitiveActionForm(FlaskForm):
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired()])

class CategoryForm(FlaskForm):
    name = StringField('Category Name', validators=[DataRequired(), Length(max=100)])
    code = StringField('Category Code', validators=[DataRequired(), Length(max=30)])
    description = TextAreaField('Description', validators=[Optional()])
    status = SelectField('Status', choices=[('Active', 'Active'), ('Inactive', 'Inactive')], default='Active')

class SupplierForm(FlaskForm):
    name = StringField('Supplier Name', validators=[DataRequired(), Length(max=100)])
    phone = StringField('Phone', validators=[DataRequired(), Length(max=20)])
    email = StringField('Email', validators=[Optional(), Email()])
    gst_number = StringField('GST Number', validators=[Optional(), Length(max=30)])
    address = TextAreaField('Address', validators=[Optional()])
    status = SelectField('Status', choices=[('Active', 'Active'), ('Inactive', 'Inactive')], default='Active')

class CustomerForm(FlaskForm):
    name = StringField('Customer Name', validators=[DataRequired(), Length(max=100)])
    phone = StringField('Phone Number', validators=[DataRequired(), Length(max=20)])
    email = StringField('Email', validators=[Optional(), Email()])
    address = TextAreaField('Address', validators=[Optional()])
    status = SelectField('Status', choices=[('Active', 'Active'), ('Inactive', 'Inactive')], default='Active')

class ProductForm(FlaskForm):
    name = StringField('Product Name', validators=[DataRequired(), Length(max=150)])
    sku = StringField('SKU Code', validators=[DataRequired(), Length(max=50)])
    barcode = StringField('Barcode', validators=[Optional(), Length(max=50)])
    category_id = SelectField('Category', coerce=int, validators=[DataRequired()])
    supplier_id = SelectField('Supplier', coerce=int, validators=[Optional()])
    brand = StringField('Brand', validators=[Optional(), Length(max=100)])
    
    purchase_price = FloatField('Purchase Price', validators=[DataRequired(), NumberRange(min=0)])
    selling_price = FloatField('Selling Price', validators=[DataRequired(), NumberRange(min=0)])
    tax_percent = FloatField('Tax Rate (%)', validators=[Optional(), NumberRange(min=0, max=100)], default=0.0)
    discount_percent = FloatField('Discount (%)', validators=[Optional(), NumberRange(min=0, max=100)], default=0.0)
    
    quantity = IntegerField('Initial Stock Quantity', validators=[DataRequired(), NumberRange(min=0)])
    min_stock = IntegerField('Minimum Stock Level', validators=[DataRequired(), NumberRange(min=0)], default=10)
    max_stock = IntegerField('Maximum Stock Level', validators=[DataRequired(), NumberRange(min=1)], default=500)
    
    expiry_date = DateField('Expiry Date', validators=[Optional()])
    mfd_date = DateField('Manufacturing Date', validators=[Optional()])
    unit = SelectField('Unit', choices=[('pcs', 'Pieces (pcs)'), ('kg', 'Kilogram (kg)'), ('g', 'Gram (g)'), ('l', 'Liter (l)'), ('ml', 'Milliliter (ml)'), ('box', 'Box'), ('pkt', 'Packet')], default='pcs')
    
    image = FileField('Product Image', validators=[Optional()])
    status = SelectField('Status', choices=[('Active', 'Active'), ('Inactive', 'Inactive')], default='Active')
    notes = TextAreaField('Notes', validators=[Optional()])

class StockAdjustmentForm(FlaskForm):
    change_type = SelectField('Adjustment Type', choices=[('Stock In', 'Stock In (+)'), ('Stock Out', 'Stock Out (-)'), ('Adjustment', 'Inventory Audit Correction')], default='Stock In')
    quantity_changed = IntegerField('Quantity', validators=[DataRequired()])
    reason = StringField('Reason / Note', validators=[DataRequired(), Length(max=255)])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired()])

class SettingForm(FlaskForm):
    store_name = StringField('Store Name', validators=[DataRequired()])
    gst_number = StringField('Store GST Number', validators=[Optional()])
    phone = StringField('Phone', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    currency = StringField('Currency Symbol', validators=[DataRequired()], default='₹')
    invoice_prefix = StringField('Invoice Prefix', validators=[DataRequired()], default='INV')
    tax_percentage = FloatField('Default Tax Rate (%)', validators=[Optional(), NumberRange(min=0, max=100)], default=5.0)

class ProfileForm(FlaskForm):
    full_name = StringField('Full Name', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    current_password = PasswordField('Current Password', validators=[Optional()])
    new_password = PasswordField('New Password', validators=[Optional(), Length(min=6)])

class UserForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=3, max=50)])
    full_name = StringField('Full Name', validators=[DataRequired(), Length(max=100)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[Optional(), Length(min=6)])
    role = SelectField('Role', choices=[('Admin', 'Admin'), ('Manager', 'Manager'), ('Cashier', 'Cashier')], default='Cashier')
    status = SelectField('Status', choices=[('Active', 'Active'), ('Inactive', 'Inactive')], default='Active')

