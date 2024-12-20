import sublime, sublime_plugin, re, os, subprocess, urllib.request, urllib.parse, io


class CombinerCommand(sublime_plugin.TextCommand):
    def run(self, edit):
        
        # ---
        # definimos variables iniciales
        # ---
        full_name = self.view.file_name()
        extension = full_name.split('.')[-1]
        file_name = '.'.join(full_name.split('.')[0:-1])
        file=full_name.split('\\')[-1]
        path=full_name.split(file)[0]

        allcontent = sublime.Region(0, self.view.size())
        allcontent = self.view.substr(allcontent)


        # path='W:/XAMPP/htdocs/OnClick/WORKS/Ubisoft/ACO/ACO - Foto/web/'
        # print (path)
        # print (file_name)
        # print (full_name)
        # print (archive_output)
        # print (allcontent)

        # ---
        # Los patters de extraer los strings
        # ---
        pattern_block = 'Combiner.*?\}'
        pattern_online = 'http'
        pattern_file = '/{0,2}combine:*\"(.+)\" *,'
        pattern_output= '/{0,2}output:*\"(.+)\" *'

        # ---
        # Bucle cogiendo cada bloque de combiner presente en el archivo
        # ---
        for temp_block in re.findall(pattern_block,allcontent,re.DOTALL):
            online_file = False
            archive_list=""
            temp_content=""
            # print("---->")
            # print(temp_block)

            #---
            # loop cogiendo los elementos a concatenar
            # ---
            for m in re.finditer(pattern_file, temp_block):

                # print('found:', m.start(), m.end())
                temp_name =sublime.Region(m.start(), m.end())
                temp_name = self.view.substr(temp_name)
                temp_name= m.group(1)
                # print(temp_name)
                # archive_list=archive_list+" "+path+temp_name

                # miramos si es online y cogemos su contenido o lo metemos en la lista del concat
                if temp_name.find(pattern_online) != -1:
                    online_file = True
                    urlopen = urllib.request.urlopen
                    content = urlopen(temp_name).read().decode('utf-8')
                    temp_content=temp_content+"\n"+content
                    # print(content)
                    # print("online!!!")
                else:
                    # opcion inicial para concat
                    archive_list=archive_list+" "+path+temp_name

                    # probamos a abrir el archivo
                    f = open(path+temp_name)
                    content = f.read()
                    temp_content=temp_content+"\n"+content
                    # print(content)

            #---
            # cogemos el archivo de destino
            #---
            try:
                archive_output = re.search(pattern_output,temp_block).group(1)
                archive_output = path + archive_output
            except AttributeError:
                archive_output = file_name + '.comb.' + extension

            # print(archive_output)

            # ---
            # con todo definido ejecutamos el concatenado o metemos los remotos en el archivo unico
            # ---
            # if online_file == False:
            #     arguments=archive_output+archive_list
            #     print ("-> concat -o "+arguments)
            #     USE_SHELL = sublime.platform() == 'windows'
            #     POPEN_ENV = ({'PATH': ':'.join(['/usr/local/bin', os.environ['PATH']])}) if sublime.platform() == 'osx' and os.path.isdir('/usr/local/bin') else None
            #     cmd="concat -o "+arguments
            #     subprocess.Popen(cmd, stderr=subprocess.PIPE, shell=USE_SHELL, env=POPEN_ENV)

            # else:
                # print(temp_content)

                # view = self.view
                # window = view.window()
                # new_view = window.new_file()
                # new_view.set_name(archive_output)
                # new_view.insert(edit, 0, temp_content)
                # new_view.end_edit(edit)
                # new_view.run_command("save")
                # window.run_command("build")

            # si no existe esa carpeta que la cree
            from os.path import dirname
            # print (dirname(archive_output))
            carpetas=dirname(archive_output)
            if not os.path.exists(carpetas):
                os.makedirs(carpetas)

            file = open(archive_output, 'w')
            file.write(temp_content)
            file.close()
 
            # despues abrimos el archivo generado
            sublime.active_window().open_file(archive_output)



class MinifyCommand(sublime_plugin.TextCommand):
    def run(self, edit):
        print ("Combiner > Minify updated?")

        # ---
        # definimos variables iniciales -> igual que en la funcion de arriba
        # ---
        full_name = self.view.file_name()
        extension = full_name.split('.')[-1]
        file_name = '.'.join(full_name.split('.')[0:-1])
        file=full_name.split('\\')[-1]
        path=full_name.split(file)[0]

        # allcontent = sublime.Region(0, self.view.size())
        # allcontent = self.view.substr(allcontent)

        # full_name = self.view.file_name()
        # print (full_name)

        # definimos la ruta a hacer la llamada
        # print (extension)

        
        # if extension == "js":
        if extension == "js":
            url = 'https://www.toptal.com/developers/javascript-minifier/api/raw'
        elif extension == "css":
            url = 'https://www.toptal.com/developers/cssminifier/api/raw'
        elif extension == "html":
            url = 'https://www.toptal.com/developers/html-minifier/api/raw'
        elif extension == "htm":
            url = 'https://www.toptal.com/developers/html-minifier/api/raw'
        else:
            print ("no compatible file")

        # cogemos los datos de nuestro archivo seleccionado/abierto
        data = {'input': open(full_name, 'rb').read()}
        data = bytes( urllib.parse.urlencode( data ).encode("utf-8") )

        #llamamos a la url y le pasamos los datos del archivo
        # handler = urllib.request.urlopen( url, data ); # esta linea de error


        user_agent = 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.9.0.7) Gecko/2009021910 Firefox/3.0.7'
        headers={'User-Agent':user_agent,} 
        request=urllib.request.Request(url,None,headers) #The assembled request
        handler = urllib.request.urlopen(request,data)
        # data = response.read() # The data u need


        #a partir de aqui estaria igual
        temp_content = handler.read().decode("utf-8")



        # definimos el nombre y metemos el contenido devuelto dentro del archivo
        archive_output = file_name + '.min.' + extension


        # file = open(archive_output, 'w')
        # file.write(temp_content)
        # file.close()


        file = io.open(archive_output, 'w',encoding='utf8')
        file.write(temp_content)
        file.close()



        # with io.open(archive_output,'r') as f:
            # text = f.read()
        # process Unicode text
        # with io.open(archive_output,'w',encoding='utf8') as f:
            # f.write(text)



        # despues abrimos el archivo generado
        sublime.active_window().open_file(archive_output)
        
        # set_encoding("utf-8")


# class EventListener(sublime_plugin.EventListener):
        # def on_load ( file, view ):
        #     # print("--> "+archive_output)
        #     print("--> "+view.file_name())

        #     # print("CUALTIENE?")
        #     codificacion=view.encoding()
        #     # if(codificacion=="Western (Windows 1252)")
        #     print("CUALTIENE? " + codificacion)

            # print("METEMOS EL UTF-8")
            # view.set_encoding("utf-8")
            # view.run_command("save")





        # fileExtension = view.window().extract_variables() [ "file_extension" ]

        # encodingSets = \
        #     {
        #         "log"  : "Hexadecimal",
        #         "dump" : "Hexadecimal",
        #     }

        # if fileExtension in encodingSets:
        #     encoding = encodingSets[ fileExtension ]
        #     view.run_command ( "reopen", { "encoding" : encoding } )