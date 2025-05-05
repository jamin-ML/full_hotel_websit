from django import template
register = template.Library() #registering this modul as django template library
# This allows us to create custom template tags and filters called add_class
@register.filter(name="add_class")
#add a css class to a field widget in for styling 
def  add_class(field,css):
    return field.as_widget(attrs={'class':css})
