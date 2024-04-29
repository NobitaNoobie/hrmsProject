Python Json
1. json.dumps(python data) -> json data ; ised to convert python dictionary to JSON data
2. json.loads(data) -> this is used to parse JSON string into python dictionary


Serializers
In Django REST framework, serializers are responsible for converting complex data such as querysets and model instances to native Python Datatypes(called serialization) that can then be easily rendered into JSON, XML or other content types which is understandable by frontend.

Serializers are also responsible for deserialization which means it allows the parsed data to be converted back into complex types, after first validating the incoming data.

1. Serialization process
    * A serializer class is very similar to a Django form and ModelForm class, that includes similar validation flags on the various fields, such as required, max_length, and default
    * DRF provides __Serializer class__, __ModelSerializer class__(shortcut method)

* Option 1: using Serializer class: 
        1. create a serializers.py file to write all serializers
        2. from rest_framework import serializers
        3. class ModelNameSerializer(serializers.Serializer):
        #this class is inheriting the Serializer class
        field_name1 = serializers.CharField(max_length = 100)
        field_name2 = serializers.IntegerField()
        field_name3 =
        serializers.CharField(max_length = 100) 

* Option 2: Using ModelSerializer
    The process of converting complex data such as querysets and model instances to native Python datatypes are called as Serialization in DRF.

    1. Creating an object of the Model class
        model_object = ModelName.objects.get(id = 1)
    2. Converting model object to Serializing object / Python dict
        serializer = ModelNameSerializer(model_object)
    3.  model_object = ModelName.objects.all()
        serializer = ModelNameSerializer(model_object, many=True)
        import rest_framework.renderers import JSONRenderer
        json_data = JSONRenderer().render(serializer.data)
    this json renderer converts the python data type serializer to frontend-readable JSON format.



