#!/usr/bin/env python

from extensions.bas_extension import BaseExtension
from config import Config
from utils import Utils
from record import Record, Tag
import os

class Edit(BaseExtension):

    def __init__(self):
        BaseExtension.__init__(self)
        self.utils = Utils()
        self.tag = Tag()

    def excute(self, form_dict):
        rID = form_dict['rID'].strip()
        rTitle = form_dict['rTitle'].strip()
        fileName = form_dict['originFileName'].strip()
        originFileName = form_dict['originFileName'].strip()
        divID = form_dict['divID']
        if form_dict.has_key('textContent'):
            textContent = form_dict['textContent']
            library = ''
            if form_dict['fileName'].strip().endswith('-library'):
                library = form_dict['fileName'][form_dict['fileName'].rfind('/') + 1 :].strip()
            return self.editRecord(rID, self.utils.removeDoubleSpace(textContent.replace('\n', ' ')), originFileName, library=library)
            
        print fileName
        r = self.utils.getRecord(rID, path=fileName, use_cache=False)
        html = 'not found'
        areaID = rID.replace(' ', '-').replace('.', '-') + '-area'
        if r != None and r.get_id().strip() != '':
            column = str(form_dict['column'])
            rows = '25'
            cols = '75'
            if column == '1':
                rows = '45'
                cols = '99' 
            elif column == '2':
                rows = '35'
                cols = '88'
            desc = r.get_describe().strip()
            html = ''
            print form_dict['extension_count']
            print desc
            if int(form_dict['extension_count']) > 12:
                html += '<br>'
            html += '<textarea rows="' + rows + '" cols="' + cols + '" id="' + areaID + '" style="font-size: 13px; border-radius:5px 5px 5px 5px;" '
            html += 'onfocus="setbg(' + "'" + areaID + "'," + "'#e5fff3');" + '" '
            html += 'onblur="setbg(' + "'" + areaID + "'," + "'white');" + '">'
            start = 0
            if rID.startswith('custom-'):
                html += 'id:' + r.get_id().strip() + '\n'
                html += '\ntitle:' + r.get_title().strip() + '\n'
            else:
                html += 'title:' + r.get_title().strip() + '\n'
            html += '\nurl:' + r.get_url().strip() + '\n'

            library = ''
            if form_dict['fileName'].strip().endswith('-library'):
                library = form_dict['fileName'][form_dict['fileName'].rfind('/') + 1 :].strip()
            #print 'library:----' + library
            while start < len(desc):
                end = self.utils.next_pos(desc, start, int(cols), self.tag.get_tag_list(library), library=library) 
                #print end
                line = desc[start : end].strip()
                
                print line
                if line.find(':') != -1 and line.find(':') < 15 and line[0 : 1].islower():
                    line = '\n' + line
                html += line + '\n'
                

                if end < 0 or line.strip() == '':
                    break
                start = end

            html += '</textarea>'
            script = "var text = $('#" + areaID + "'); console.log('', text[0].value);"
            script += "var postArgs = {name : 'edit', rID : '" + rID + "', rTitle : '" + rTitle +"', check: 'false', fileName : '" + fileName + "', divID : '" + divID + "', originFileName : '" + originFileName+ "', textContent: text[0].value};";
            linkid = divID.replace('-edit', '').replace('div', 'a')
            script += "$.post('/extensions', postArgs, function(data) { window.location.href = window.location.href.replace('#', ''); });"
            # var a = document.getElementById('" + linkid + "'); var evnt = a['onclick']; evnt.call(a);

            html += '<br><button type="submit" id="edit_btn" hidefocus="true" onclick="' + script + '">submit</button>'
        return html

    def editRecord(self, rID, data, originFileName, library=''):
        print data
        record = Record(' | | | ' + data)
        newid = self.utils.reflection_call('record', 'WrapRecord', 'get_tag_content', record.line, {'tag' : 'id'})
        if newid != None:
            newid = newid.strip()
        title = self.utils.reflection_call('record', 'WrapRecord', 'get_tag_content', record.line, {'tag' : 'title', 'library' : library}).strip()
        url = self.utils.reflection_call('record', 'WrapRecord', 'get_tag_content', record.line, {'tag' : 'url', 'library' : library}).strip()
        desc = data.replace('title:' + title, '').replace('url:' + url, '').strip()
        print rID
        print title 
        print url
        print desc
        newline = ''
        if rID.startswith('custom-'):
            desc = desc.replace('id:' + newid, '').strip()
            newline = newid + ' | ' + title + ' | ' + url + ' | ' + desc + '\n'
        else:
            newline = rID + ' | ' + title + ' | ' + url + ' | ' + desc + '\n'
        print 'newline:'
        print newline
        if os.path.exists(originFileName):
            f = open(originFileName, 'rU')
            all_lines = []
            for line in f.readlines():
                if rID != line[0 : line.find('|')].strip():
                    all_lines.append(line)
                else:
                    print 'old line:'
                    print line
                    all_lines.append(newline)
            f.close()
            
            f = open(originFileName, 'w')
            if len(all_lines) > 0:
                for line in all_lines:
                    f.write(line)
            else:
                f.write('')
                f.close()
            
            return 'refresh'
        return 'error'



    def check(self, form_dict):
        rID = form_dict['rID'].strip()
        return rID.startswith('loop') == False
