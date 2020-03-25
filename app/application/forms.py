from django import forms
from .models import SampleApplication_Db, PlateProperties_Db
from django.contrib.auth.models import User

class SampleApplicationForm(forms.ModelForm):
    filename =forms.CharField(label='Save', max_length=16,required=False,
        widget = forms.TextInput(attrs={
                    'id':'filename',
                    'name': 'filename',
                    'class':'form-control',
                    'value': '',
                    'placeholder':'Filename',
                    'size':'14'
                }
            )
        )

    motorspeed = forms.CharField(label='MotorSpeed', max_length=16,required=False,
        widget = forms.TextInput(attrs={
                    'id':'resumemotorspeed',
                    'name': 'motorspeed',
                    'value': '',
                    'style': 'border-width:0px; background-color:transparent',
                    'readonly': 'readonly',
                    'size':'14'
                }
            )
        )
    pressure = forms.CharField(label='Pressure', max_length=16,required=False,
        widget = forms.TextInput(attrs={
                    'id':'resumepressure',
                    'name': 'pressure',
                    'value': '',
                    'style': 'border-width:0px; background-color:transparent',
                    'readonly': 'readonly',
                    'size':'14'
                }
            )
        )
    deltapressure = forms.CharField(label='Pressure', max_length=16,required=False,
        widget = forms.TextInput(attrs={
                    'id':'resumepressure',
                    'name': 'pressure',
                    'value': '',
                    'style': 'border-width:0px; background-color:transparent',
                    'readonly': 'readonly',
                    'size':'14'
                }
            )
        )

    sizes = forms.CharField(label='Sizes', max_length=16,required=False,
        widget = forms.TextInput(attrs={
                    'id':'resumesizes',
                    'name': 'sizes',
                    'value': '',
                    'style': 'border-width:0px; background-color:transparent',
                    'readonly': 'readonly',
                    'size':'15'
                }
            )
        )
    offsets = forms.CharField(label='Offsets', max_length=16,required=False,
        widget = forms.TextInput(attrs={
                    'id':'resumeoffsets',
                    'name': 'offsets',
                    'value': '',
                    'style': 'border-width:0px; background-color:transparent',
                    'readonly': 'readonly',
                    'size':'14'
                }
            )
        )
    bandproperties = forms.CharField(label='Bands Properties', max_length=16,required=False,
        widget = forms.TextInput(attrs={
                    'id':'resumebandproperties',
                    'name': 'bandproperties',
                    'value': '',
                    'style': 'border-width:0px; background-color:transparent',
                    'readonly': 'readonly',
                    'size':'14'
                }
            )
        )

    nbands = forms.CharField(label='N° Bands', max_length=16,required=False,
        widget = forms.TextInput(attrs={
                    'id':'resumenbands',
                    'name': 'nbands',
                    'value': '',
                    'style': 'border-width:0px; background-color:transparent',
                    'readonly': 'readonly',
                    'size':'14'
                }
            )
        )
    lengthbands = forms.CharField(label='Length Bands', max_length=16,required=False,
        widget = forms.TextInput(attrs={
                    'id':'resumelengthbands',
                    'name': 'lengthbands',
                    'value': '0',
                    'style': 'border-width:0px; background-color:transparent',
                    'readonly': 'readonly',
                    'size':'14'
                }
            )
        )
    height = forms.CharField(label='Height', max_length=16,required=False,
        widget = forms.TextInput(attrs={
                    'id':'resumeheigth',
                    'name': 'height',
                    'value': '',
                    'style': 'border-width:0px; background-color:transparent',
                    'readonly': 'readonly',
                    'size':'14'
                }
            )
        )
    gap = forms.CharField(label='Gap', max_length=16,required=False,
        widget = forms.TextInput(attrs={
                    'id':'resumegap',
                    'name': 'gap',
                    'value': '',
                    'style': 'border-width:0px; background-color:transparent',
                    'readonly': 'readonly',
                    'size':'14'
                }
            )
        )

    plate_properties = dict()
    band_settings = dict()

    class Meta:
        model = SampleApplication_Db
        fields = ('motorspeed','pressure','deltapressure',)

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user')
        super(SampleApplicationForm, self).__init__(*args, **kwargs)

    def clean(self):
        finaldict = self.cleaned_data.copy()

        finaldict['pressure'] = self.formatdata(self.cleaned_data['pressure'])[0]
        finaldict['deltapressure'] = self.formatdata(self.cleaned_data['pressure'])[1]
        auxsizes = self.formatdata(self.cleaned_data['sizes'])
        auxpressure = self.formatdata(self.cleaned_data['offsets'])
        self.plate_properties['sizex'] = auxsizes[0]
        self.plate_properties['sizey'] = auxsizes[1]
        self.plate_properties['offsetx'] = auxpressure[0]
        self.plate_properties['offsety'] = auxpressure[1]

        self.band_settings['bandsetting'] = self.cleaned_data['bandproperties']
        self.band_settings['nbands'] = self.cleaned_data['nbands']
        self.band_settings['lengthbands'] = self.cleaned_data['lengthbands']
        self.band_settings['height'] = self.cleaned_data['height']
        self.band_settings['gap'] = self.cleaned_data['gap']

        del finaldict['sizes']
        del finaldict['offsets']

        finaldict.update(self.plate_properties)

        # Verify that the if nbands is selected, then nbands value should be !=0
        if self.band_settings['bandsetting'] == 'N° Bands' and int(self.band_settings['nbands']) <= 0:
            raise forms.ValidationError("Invalid Data")
        if self.band_settings['bandsetting'] == 'Length' and int(self.band_settings['lengthbands']) == 0:
            raise forms.ValidationError("Invalid Data")

        return finaldict

    def clean_motorspeed(self):
        motorspeed = self.cleaned_data['motorspeed']
        if motorspeed == '':
            motorspeed = 0
        return motorspeed

    # def clean_filename(self):
        # IMPLEMENT IN DB VALIDATOR
        # filename = self.cleaned_data['filename']
        # try:
        #     in_db=SampleApplication_Db.objects.filter(filename=filename).filter(auth_id=self.user)
        #     if len(in_db)>0:
        #         raise forms.ValidationError("File already exist")
        # except SampleApplication_Db.DoesNotExist:
            # return filename

    def formatdata(self,data):
        lista = data.split(',')
        res=[]
        for sub in lista:
            if ','in sub:
                try:
                    res.append(int(sub.split(':')[1]))
                except ValueError:
                    res.append('0')
            else:
                try:
                    res.append(float(sub.split(':')[1]))
                except ValueError:
                    res.append('0')
        return res
