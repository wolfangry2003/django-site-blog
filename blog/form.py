from django import forms

class ContactForm(forms.Form):
    email = forms.EmailField(max_length=200, label='آدرس ایمیل', help_text= '.لطفا ایمیل درستی را وارد کنید زیرا با همین ایمیل مورد نظر با شما تماس خواهیم گرفت')
    message = forms.CharField(widget=forms.Textarea, label='پیام', help_text='.لطفا اول پیام اسم خود را قرار دهید با تشکر ادمین سایت')


