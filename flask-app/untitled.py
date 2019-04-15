import subprocess

password = 'PCT4life!'
start_date = '01/01/2003'
batch_dir = 'Z:\\Data Analytics\\0. Projects\\Fleet Smooth Replacement Plan\\data\\batch\\'
output_dir = 'C:\\Users\\bvanderblock\\Desktop'
batch_name = 'fleet_vehicles_batch_1.csv'
file_name = 'export-test-2.XLSX'

subprocess.call(['cscript.exe', '''
If Not IsObject(application) Then
   Set SapGuiAuto  = GetObject("SAPGUI")
   Set application = SapGuiAuto.GetScriptingEngine
End If
If Not IsObject(connection) Then
   Set connection = application.Children(0)
End If
If Not IsObject(session) Then
   Set session    = connection.Children(0)
End If
If IsObject(WScript) Then
   WScript.ConnectObject session,     "on"
   WScript.ConnectObject application, "on"
End If
session.findById("wnd[0]").maximize
session.findById("wnd[0]/usr/txtRSYST-BNAME").text = "bvanderblock"
session.findById("wnd[0]/usr/pwdRSYST-BCODE").text = "'''
+
password
+
'''"
session.findById("wnd[0]/usr/pwdRSYST-BCODE").setFocus
session.findById("wnd[0]/usr/pwdRSYST-BCODE").caretPosition = 9
session.findById("wnd[0]").sendVKey 0
session.findById("wnd[0]/usr/cntlIMAGE_CONTAINER/shellcont/shell/shellcont[0]/shell").expandNode "F00003"
session.findById("wnd[0]/usr/cntlIMAGE_CONTAINER/shellcont/shell/shellcont[0]/shell").selectedNode = "F00006"
session.findById("wnd[0]/usr/cntlIMAGE_CONTAINER/shellcont/shell/shellcont[0]/shell").topNode = "Favo"
session.findById("wnd[0]/usr/cntlIMAGE_CONTAINER/shellcont/shell/shellcont[0]/shell").doubleClickNode "F00006"
session.findById("wnd[1]").sendVKey 4
session.findById("wnd[2]/usr/lbl[1,7]").setFocus
session.findById("wnd[2]/usr/lbl[1,7]").caretPosition = 1
session.findById("wnd[2]/tbar[0]/btn[0]").press
session.findById("wnd[1]/tbar[0]/btn[0]").press
session.findById("wnd[0]/usr/ctxtR_BUDAT-LOW").text = "'''
+
start_date
+
'''"
session.findById("wnd[0]/usr/ctxtAUFNR-LOW").setFocus
session.findById("wnd[0]/usr/ctxtAUFNR-LOW").caretPosition = 0
session.findById("wnd[0]/usr/btn%_AUFNR_%_APP_%-VALU_PUSH").press
session.findById("wnd[1]/tbar[0]/btn[23]").press
session.findById("wnd[2]/usr/ctxtDY_PATH").text = "'''
+
batch_dir
+
'''"
session.findById("wnd[2]/usr/ctxtDY_FILENAME").text = "'''
+
batch_name
+
'''"
session.findById("wnd[2]/usr/ctxtDY_FILENAME").caretPosition = 26
session.findById("wnd[2]/tbar[0]/btn[0]").press
session.findById("wnd[1]/tbar[0]/btn[8]").press
session.findById("wnd[0]/tbar[1]/btn[8]").press
session.findById("wnd[0]/tbar[1]/btn[43]").press
session.findById("wnd[1]/usr/ctxtDY_PATH").text = "'''
+
output_dir
+
'''"
session.findById("wnd[1]/usr/ctxtDY_FILENAME").text = "'''
+
file_name
+
'''"
session.findById("wnd[1]/tbar[0]/btn[0]").press'''])