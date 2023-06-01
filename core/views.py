from django.shortcuts import render,redirect,HttpResponse
from core.models import Function
import ast

def home(request):
    return redirect('/all')

def all(request):
    functions = Function.objects.all()
    return render(request,"all.html",{'functions':functions})

def add(request):
    if request.method == "GET":
        return render(request,'add.html')
    elif request.method == "POST":
        name = request.POST.get('name')
        params_count = int(request.POST.get('params-count'))
        code = request.POST.get('code')
        params = {}
        for i in range(params_count):
            params[request.POST.get(f'param-{i+1}')] = request.POST.get(f'param-type-{i+1}')  # noqa: E501
        function = Function(name=name,code=code,params=str(params))
        function.save()
        return redirect('/all')
    
def delete(request,id):
    function = Function.objects.get(id=id)
    function.delete()
    return redirect('/all')

def edit(request,id):
    if(request.method == "GET"):
        function = Function.objects.get(id=id)
        params = ast.literal_eval(function.params)
        return render(request,'edit.html',{'function':function,'params':params})
    elif request.method == "POST":
        function = Function.objects.get(id=id)
        function.name = request.POST.get('name')
        function.code = request.POST.get('code')
        function.save()
        return redirect('/all')
    
def exec_func(request,id):
    if request.method=="GET":
        function = Function.objects.get(id=id)
        params = ast.literal_eval(function.params)
        return render(request,"get_params.html",{'params':params,'id':id,'code':function.code})
    if request.method=="POST":
        function = Function.objects.get(id=id)
        # Adding params to the code
        params = ast.literal_eval(function.params)            
        code = ""
        for i in params.keys():
            if params[i] != 'str':
                code += f"{i}={ast.literal_eval(request.POST.get(i))}\n"
            else:
                code += f"{i}='{request.POST.get(i)}'\n"

        # writing output of function to file
        f = open('output.txt','w')
        f_code = function.code
        code_lines = f_code.splitlines()
        for i in code_lines[-1:-100:-1]:
            if i == "":
                continue
            else:
                if "return" in code_lines[-1]:
                    code_lines[-1]=code_lines[-1].replace('return',"f.write(str(")+"))"
                break
        for i in code_lines:
            if "print" in i:
                i = i.replace('print(',"f.write(str(")+')'
            code+=i+"\n"

        print(code)
        exec_obj = compile(code,'mulstring','exec')
        exec(exec_obj)
        f.close()

        f = open('output.txt','r')
        output = f.read()
        f.close()
        return render(request,'output.html',{'output':output})