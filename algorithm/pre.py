
import os
from str_replace import str_replace
from TF_IDF.StrToUni import StrToUni
import GrobalParament
from full_word_cut import fullcut
from half_word_cut import halfcut
from UniToStr import UniToStr



def prepro_file(fl_in_url,re_out_url,*wd_be_del):
    in_url=fl_in_url.replace('\\','/')
    out_url=re_out_url.replace('\\','/')
    try:
        try:
            fl_in=os.listdir(in_url)
        except WindowsError:
            print "输入的预处理文档目录有误"
        try:
            re_out=open(out_url,'w')
        except WindowsError:
            print "输入的结果文档输出目录有误"
    except NameError:
        pass
    else:
        for file in fl_in:
            afile_url=fl_in_url+'/'+file
            if os.path.isfile(afile_url):
                afile=open(afile_url,"r")
                content_temp="".join(afile.readlines())
                if not wd_be_del:
                    content=str_replace(content_temp,"","\t","\n"," ")#删除某些特殊字符如\t,\n等以保证是一行的连续的
                else:
                    content=str_replace(content_temp,'',*wd_be_del)
                con_unicode=StrToUni(content,*(GrobalParament.InputFormatList))
                if GrobalParament.pattern=="full":
                    cut_result=fullcut(con_unicode)
                else:
                    cut_result=halfcut(con_unicode)
                s_fl_Name=UniToStr(file,*(GrobalParament.OutputFormatList))
                re_out.write(s_fl_Name+'\t')
                key_word_out=[]
                for key_word in cut_result:
                    s_key_word=UniToStr(key_word,*(GrobalParament.OutputFormatList))
                    key_word_out.append(s_key_word)
                out_str=','.join(key_word_out)
                re_out.write(out_str)
                re_out.write('\n')

    #def str_replace(str_source, char, *words):
                    #str_temp = str_source
                    #for word in words:
                        #str_temp = str_temp.replace(word, char)
                    #return str_temp

    #def StrToUni_try(str, type_1):
        #try:
            #str.decode(type_1)
        #except UnicodeDecodeError:
            #return False
        #else:
            #return True

    #def StrToUni(str, *type_list):
        #if not type_list:
            #if StrToUni_try(str, 'utf-8'):
                #return str.decode('utf-8')
            #else:
                #print "输入的源文件的编码格式不是utf-8"
        #else:
            #for type_2 in type_list:
                #if StrToUni_try(str, type_2):
                    #return str.decode(type_2)
                #else:
                    #if type_2 == type_list[-1]:
                        #print "输入的源文件的编码格式不在您提供的格式列表中"

    #def UniToStr_try(str, type_1):
        #try:
            #str.encode(type_1)
        #except LookupError:
            #return False
        #else:
            #return True

    #def UniToStr(str, *out_Format):
        #if not out_Format:
            #return str.encode('utf-8')
        #else:
            #for type_2 in out_Format:
                #if UniToStr_try(str, type_2):
                    #return str.encode(type_2)
                #else:
                    #if type_2 == out_Format[-1]:
                        #print "输入的目标编码格式不正确"