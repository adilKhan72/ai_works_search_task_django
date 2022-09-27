from django.shortcuts import render
from django.templatetags.static import static

from pathlib import Path
import json
import pandas as pd
import objectpath


BASE_DIR = Path(__file__).resolve().parent.parent
# Create your views here.
def index(request):
    final_result = dict()
    search_string = ""
    request_type = request.method
    files_to_search = list(('organizations.json', 'tickets.json', 'users.json'))
    if request.method == "POST":
        search_string = request.POST["search_string"]
        for index_file, file_name in enumerate(files_to_search):
            with open(BASE_DIR / 'static/{}'.format(file_name), 'r') as myfile:
                data = myfile.read()
            json_file = json.loads(data)
            result = list()
            count_div = 0
            for index_list, item_list in enumerate(json_file):
                searched = False
                for key_dic, value_dic in item_list.items():
                    if searched == False:
                        if isinstance(value_dic, (int, float, str)):
                            if search_string.strip() != "":
                                if search_string.strip() in str(value_dic):
                                    result.append(item_list)
                                    searched = True
                                    count_div += 1
                                    continue 
                            else:
                                value_dic = str(value_dic)
                                if value_dic.strip() == "":
                                    result.append(item_list)
                                    searched = True
                                    count_div += 1
                                    continue 
                        if isinstance(value_dic, list):
                            for index_list_inner, item_list_inner in enumerate(value_dic):
                                if search_string.strip() != "":
                                    if search_string.strip() in str(item_list_inner):
                                        result.append(item_list)
                                        searched = True
                                        count_div += 1
                                        continue
                                else:  
                                    item_list_inner = str(item_list_inner)
                                    if item_list_inner.strip() == "":
                                        result.append(item_list)
                                        searched = True
                                        count_div += 1
                                        continue
                        if count_div == 3:
                            count_div = 0
                            result.append({'row_for_divs': '</div><div class="row">'})
            final_result[file_name] = result
    context = {
        "search_string" : search_string,
        "final_result" : final_result,
        "request.method" : request_type
    }
    return render(request, "index.html", context)

def about(request):
    return render(request, "about.html")