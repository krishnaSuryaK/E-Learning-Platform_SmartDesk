def handle_uploaded_file_mccp(f,name):  
    with open('quiz/static/upload/MCCP/'+name+" "+f.name, 'wb+') as destination:  
        for chunk in f.chunks():  
            destination.write(chunk)

def handle_uploaded_file_os(f,name):  
    with open('quiz/static/upload/OS/'+name+" "+f.name, 'wb+') as destination:  
        for chunk in f.chunks():  
            destination.write(chunk)


def handle_uploaded_file_wt(f,name):  
    with open('quiz/static/upload/WT/'+name+" "+f.name, 'wb+') as destination:  
        for chunk in f.chunks():  
            destination.write(chunk)

def handle_uploaded_file_dm(f,name):  
    with open('quiz/static/upload/DM/'+name+" "+f.name, 'wb+') as destination:  
        for chunk in f.chunks():  
            destination.write(chunk)

def handle_uploaded_file_ai(f,name):  
    with open('quiz/static/upload/AI/'+name+" "+f.name, 'wb+') as destination:  
        for chunk in f.chunks():  
            destination.write(chunk)