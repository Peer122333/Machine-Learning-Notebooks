from IPython.display import HTML, display
import inspect

def set_background(color):    
    script = (
        "var cell = this.closest('.jp-CodeCell');"
        "var editor = cell.querySelector('.jp-Editor');"
        "editor.style.background='{}';"
        "this.parentNode.removeChild(this)"
    ).format(color)
    
    display(HTML('<img src onerror="{}" style="display:none">'.format(script)))


class Grader():
    grader = None
    token = ""

    def __init__(self):
        self.grader =    { 
        "data": { 
                'assignment_nr':"1",
                'assignment_code':"72dff619",
                'identityMatrix': {'name':'Identity Matrix', 'score':0, 'maxscore':5,'func_str': '', 'feedback':''},
                'determinantMatrix3x3': {'name':'Determinant Matrix', 'score':0,'maxscore':10, 'func_str': '', 'feedback':''},
                'transposeMatrix': {'name':'Transpose Matrix', 'score':0,'maxscore':10, 'func_str': '', 'feedback':''},
                'multiplyMatrix': {'name':'Multiply Matrix', 'score':0,'maxscore':5, 'func_str': '', 'feedback':''},
            }
        }

    def setFunc(self, id, func):
        code_str = inspect.getsource(func)
        self.grader["data"][id]["func_str"]=code_str

    def setToken(self, token):
        self.token = token

    def grade(self):
        
        
        print('\nSubmitting Solutions | Programming Exercise')

        # Evaluate the different parts of exercise

        # get results from remote
        result = self.submit()

        # Print the grading table
        if not result:
            return

        reachedScore = 0
        maxScore = 0
        for id, part in result.items():
            if "assignment_" in id:
                continue 
            score = '%d / %3d' % (part["score"], part["maxscore"])
            print('%43s | %9s | %-s' % (part["name"], score, part["feedback"]))
            reachedScore += part["score"]
            maxScore += part["maxscore"]
        total_score = '%d / %d' % (reachedScore,maxScore)
        print('                                  --------------------------------')
        print('%43s | %9s | %-s\n' % ("", total_score, ""))


    def submit(self):
        import requests
        import json

        
        url = "http://evalml.da.private.hm.edu/result_receiver/"
        
        head = {'Authorization': 'token {}'.format(self.token)}
        #head = {}
        
        response = requests.post(url, json=self.grader, headers=head)
        if response.status_code == 200:
            return response.json()
        else:
            print(f"Error: {response.status_code}")
            return False