# Kivy Libs import

# Python Lib import

# Personal Libs import
from tools.ganttool.ganttool import GantTool
from gui.widget.messagelayout import MessageLayout
from tools.notetool.notetool import NoteTool
from tools.cjsl.cjsltool import CJSLTool
from tools.exercisetool.exercisetool import ExerciseTool

def load_tool_from_id(tool_id):

    if tool_id == 10:
        return GantTool()

    elif tool_id == 11:
        return NoteTool()

    elif tool_id == 12:
        return CJSLTool()

    elif tool_id == 13:
        return ExerciseTool()


    else:
        print("this tool isn't included in your mascaret installation.")
        return MessageLayout(
        message = "this tool isn't included in your mascaret installation."
                            )
