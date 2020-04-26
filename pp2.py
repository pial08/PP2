import sys
import const
import lexanalysis
from collections import deque 
  

boolPrint = True
astTree = "\n   Program:\n"
print(astTree)

tok = lexanalysis.getNextToken()
stack = deque() 

def findCol(tok):
    return lexanalysis.find_column(lexanalysis.contents, tok)


def printBool(st):
    #print(st)
    return True

def printError(st):
    global boolPrint
    if boolPrint:
        print(st)

printBool(str(tok))

def updateTok():
    #printBool("printing from updatetok OXOXOXOXOXOXXOOXOXOXO")
    global tok
    tok = lexanalysis.getNextToken()
    printBool(str(tok))
    if tok != None:
        return True
    else:
        return False

def reportError(tok):
    global boolPrint
    if boolPrint:
        print()
        printError("*** Error line " + str(tok.lineno) + ".")
        printError(lexanalysis.lines[tok.lineno - 1])
        errorLine = ""
        length = findCol(tok) -1
        while length:
            errorLine += " "
            length -= 1
        for i in range(len(tok.value)):
            errorLine += "^"
        printError(errorLine)
        #print("column", findCol(tok), "token len", len(tok.value))
        printError("*** syntax error")
        boolPrint = False
        print()
        print()
    #pass


def Program():
    if tok == None:
        print("Empty program is syntactically incorrect.")
        return False
    printBool("inside program")
    return Decl() and  ProgramP()


def ProgramP():
    #updateTok()
    if tok != None:
        updateTok()
        if tok != None:
            return Program()
    else: 
        printBool("ending")
        return True



def Decl():
    printBool("inside decl")
    printBool(tok.value)
    if tok.value in const.typeList or tok.value == const.VOID:
        printBool("method type  found")
        updateTok()
        if tok.type == const.IDENT:
            updateTok()
            printBool("tok.value" + tok.value)
            if tok.value ==  const.LPAREN:
                return FunctionDecl()
            else:
                printBool("going to vardecl") 
                return VariableDecl() and updateTok()
    else: 
        printBool("error found")
    

def VariableDecl():
    printBool("inside var decl")
    if tok.value == const.SEMICOLON:
        printBool("semicolon found after var")
        return True
    else:
        reportError(tok)
        return False


def FunctionDecl():
    printBool("inside funcdecl")
    updateTok()
    forms  = Formals()
    
    updateTok()
    return forms  and StmtBlock()


def Formals():
    printBool("inside formals")
    if tok.value == const.RPAREN:
        return True

    while True:
        printBool("inside formal while loop....")
        if tok.value in const.typeList:
            printBool("typelist found")
            updateTok()
            if tok.type == const.IDENT:
                updateTok()
                if tok.value == const.COMMA and (updateTok() and tok.value != const.RPAREN):
                    continue
                
                elif tok.value == const.RPAREN:
                    printBool("returning from formals")
                    return True
            else:
                reportError(tok)
                return False
    
def StmtBlock():
    printBool("inside stmtBlock")
    if tok.value == const.LCURLEY:
        updateTok()
        if tok.value == const.RCURLEY:
            return True
        else:
            stmtBlckVar = VariableDeclRec() and printBool("token inside stmtBlock... " + tok.value) and  tok.value == const.RCURLEY
            updateTok()
            return stmtBlckVar
                

        """
        elif tok.value in const.typeList:
            return VariableDeclRec()
        else:
            Stmt()
        """
def VariableDeclRec():
    printBool("inside varDecRec")
    #if tok.value == const.RCURLEY:
    #        return True
    if tok.value in const.typeList and (updateTok() and tok.type == const.IDENT):
        updateTok()
        return VariableDecl() and (updateTok() and VariableDeclRec()) 
    else:
        printBool("going to statement........................")
        #return Stmt()
        while True:
            printBool("inside while loop VarDeclRec !!!!!!!!!!!!!!!!!")
            if Stmt(): 
                if tok.value == const.RCURLEY:
                    printBool("returning true from VarDeclRec")
                    return True
                if tok.value == const.ELSE:
                    printBool("else found")
                    return True
                updateTok()
                
                pass
            else:
                return True
                


def Stmt():
    
    printBool("inside stmt tok value" + str(tok))
    if tok.value == const.RCURLEY:
        printBool("returning after RCURLEY")
        return True

    #comment out due to debbuging
    #updateTok()
    if tok.value == const.IF:
        printBool("&&&&&& sending to if")
        if updateTok() and IfStmt():
            #updateTok()
            if tok.value == const.RCURLEY:
                printBool("RCURLEY found after ifSTMT......")
                return True
            else:
                return  Stmt()
    
    elif tok.value == const.WHILE:
        if updateTok() and WhileStmt():
            if tok.value == const.RCURLEY:
                printBool("RCURLEY found after WHILE_STMT......")
                return True
            else:
                printBool("STMT found instead of RCURLEY")
                return Stmt()

    #changing for
    elif tok.value == const.FOR:
        if updateTok() and ForStmt():
            if tok.value == const.RCURLEY:
                printBool("RCURLEY found after FOR_STMT......")
                return True
            else:
                printBool("STMT found instead of RCURLEY")
                return Stmt()

    #might need to add sth
    elif tok.value == const.BREAK:
        return updateTok() and BreakStmt() and updateTok() and Stmt()

    elif tok.value == const.RETURN:
        printBool("return found..............")
        return updateTok() and ReturnStmt()
    
    elif tok.value == const.PRINT: #and (updateTok() and tok.value == const.LPAREN):
        return updateTok() and PrintStmt() and updateTok() and Stmt()

    elif tok.value == const.SEMICOLON:
        printBool("semicolon found")
        return True

    elif tok.value == const.LCURLEY:
        
        return StmtBlock() and printBool("returning from stmtBlock() " + tok.value)
    
    elif Expr() and tok.value == const.SEMICOLON:
        printBool("returning after getting expr() and semicolon")
        return True
        """
        printBool("return from stmt()")
        boolVar = Expr() and tok.value == const.SEMICOLON and updateTok()
        if boolVar == True and tok.value == const.ELSE:
            return True
        else:
            return Stmt()
        """
    
        #on getting "{", code for stmt-->stmtBlock



"""
Expr ::= LValue = Expr | Constant | LValue | Call | ( Expr ) |
    Expr + Expr | Expr - Expr | Expr * Expr | Expr / Expr |
    Expr % Expr | - Expr | Expr < Expr | Expr <= Expr |
    Expr > Expr | Expr >= Expr | Expr == Expr | Expr ! = Expr |
    Expr && Expr | Expr || Expr | ! Expr | ReadInteger ( ) |
    ReadLine ( )
"""
def Expr():
    printBool("inside Expr")
    printBool(tok)

    #changed today
    """if tok.value == const.READINT:
        return True
    
    elif tok.value == const.READLINE:
        return True
    """

    if tok.value == const.LPAREN:
        printBool("((((((( leftParen found")
        #new code added and next token removed from if
        if (updateTok() and Expr()) and (printBool("*****bool print token... " + str(tok.value)) and tok.value == const.RPAREN):
            printBool("returning true.....")
            updateTok()
            if tok.value in const.operatorList:
                printBool("operator list found in lparen")
                return  updateTok() and Expr()
            else:
                return True
    


    elif tok.value == const.MINUS:
        return (updateTok() and Expr())

    elif tok.value == const.NOT:
        return updateTok() and Expr()
    
    elif tok.type == const.IDENT:
        printBool("var " + tok.value + "found")
        updateTok()
        printBool("checkpoint ...2 ")
        if tok.value == const.LPAREN:
            printBool("checkpoint ... 3")
            updateTok()
            return Actuals()
        
        elif (tok.value == const.EQUAL) or (tok.value in const.operatorList):
            printBool("equal found")
            return updateTok() and Expr()
        else: 
            
            return True
        
        #elif tok.value in const.operatorList:
        #    return updateTok() and Expr()
            
    elif tok.type in const.constantList:
        printBool("constant found")
        updateTok()
        if tok.value in const.operatorList:
            printBool("operator found after constant")
            return updateTok() and Expr()
            #return True
        elif tok.value == '.':
            updateTok()
            reportError(tok)
            return False

        else:
            #changed from return true to return Expr()
            return True
    
    
    #elif tok.value == const.RPAREN:
    #    printBool("this part executed ***********************", tok)
    #    return True
    #ReadInteger ( )
    elif tok.value == const.READINT or tok.value == const.READLINE:
        printBool("readline or readint found............................")
        if (updateTok() and tok.value == const.LPAREN) and (updateTok() and tok.value == const.RPAREN):
            updateTok()
            return True
    else:
        printBool("some error...")
        reportError(tok)
        return False


def Actuals():
    printBool("inside actuals")
    if tok.value == const.RPAREN:
        return True
    

    while True:
        printBool("tok at begin of while in actuals..." + str(tok))
        if not Expr():
            reportError(tok)
            return False
        printBool("Tok value inside actuals....." + tok)
        if tok.value == const.COMMA and (updateTok() and tok.value != const.RPAREN):
            #updateTok()
            continue
        
        if tok.value == const.RPAREN:
            updateTok()
            return True
    

    
def IfStmt():
    printBool("inside ifStmt")
    if tok.value == const.LPAREN:
        ifVar = (updateTok() and Expr()) and (printBool("if ..." + str(tok.value)) and  tok.value == const.RPAREN)
        if not ifVar:
            printBool("error inside if")
            reportError(tok)
            return False
        if updateTok() and (printBool("calling stmt() from if")) and not Stmt():
            printBool("ret false from ifStmt")
            reportError(tok)
            return False
        printBool("-----------" + str(tok))
        if tok.value == const.SEMICOLON:
            updateTok()
        
        
            
        if  tok != None and tok.value == const.ELSE:
            printBool("else found!!!")
            updateTok()
            if not Stmt():
                printBool("returning false from else*****")
                reportError(tok)
                return False 
            else:
                printBool("true for if with else------------------------------------"+ str(tok))
                return True
        else:
            printBool("true for if-----------XXXX-------------------------"+ str(tok))
            return True
    else:
        reportError(tok)
        return False


def ForStmt():
    printBool("inside FOR STMT___________________________---")
    if tok.value == const.LPAREN:
        #semicolon found for( ;  )
        printBool("lparen found")
        if updateTok() and tok.value == const.SEMICOLON:
            printBool("First expresion not found")
            pass
        # for(i = 1;)
        elif not Expr() or ( tok.value != const.SEMICOLON):
            printBool("second part is returning false")
            reportError(tok)
            return False

        # for( i = 1; i > 5;)
        printBool("token..." + str(tok))
        updateTok()
        if not Expr() or  (printBool("inside if~~~~~~~" + tok.value) and  not tok.value == const.SEMICOLON):
            printBool("third part also returning false")
            reportError(tok)
            return False 
        # for( i = 1; i > 5; )
        updateTok()
        printBool("entering final part tok = "+ str(tok))
        if tok.value == const.RPAREN:
            printBool("----------returning true from  without third part")
            return updateTok() and Stmt()

        elif Expr() and printBool("from third part......" + tok.value) and tok.value == const.RPAREN:
            printBool("++++++returning true from  with third part")
            return updateTok() and Stmt()
        
def WhileStmt():
    if tok.value == const.LPAREN:
        
        whileVar = (updateTok() and Expr()) and (printBool("while!!!!!!!!!!!!!" + str(tok.value)) and tok.value == const.RPAREN)
        if not whileVar:
            printBool("error inside while.....")
            reportError(tok)
            return False
        
        if updateTok() and not Stmt():
            printBool("false in while O_O_O_O_O_O_O_O_")
            reportError(tok)
            return False           
        printBool("true for while...."+ str(tok))
        return True
    else:
        return False


def ReturnStmt():
    printBool("inside return stmt()"+ str(tok))
    if tok.value == const.SEMICOLON:
        return True
    elif Expr()  and (tok.value == const.SEMICOLON) and updateTok():
        return True
    else:
        reportError(tok)
        return False

def BreakStmt():
    if tok.value == const.SEMICOLON:
        printBool("inside breakstmt() "+ str(tok))
        return True

#PrintStmt  --> Print ( Expr + , ) ;
#input printBool(a, " ");
def PrintStmt():
    #LPRAREN checking removed from the caller method  
    printBool("PPPPPPPPPP>>..>>>>>>>>inside print stmt"+ str(tok))
    if  tok.value == const.LPAREN: 
        while True:
            printBool("inside print loop")
            updateTok()
            if not Expr():
                printBool("returning false from printStmt")
                reportError(tok)
                return False
            if tok.value == const.COMMA:
                printBool(",,,,,,,,,,,,, comma found")
                #updateTok()
                continue
            elif tok.value == const.RPAREN:
                printBool("Rparenn found ........in print ")
                updateTok()
                printBool(tok)
                if  tok != None and tok.value == const.SEMICOLON:
                    printBool("returning true")
                    return True
                else:
                    printBool("returning false")
                    reportError(tok)
                    return False
            
    else:
        reportError(tok)
        return False
    
        
    

def main():
    printBool(Program())
    #    printBool("true")

if __name__ == "__main__":
    main()





###########""""""""""
"""
   
    elif tok.value == const.LPAREN:
        printBool("((((((( leftParen found")
        #new code added and next token removed from if
        if (updateTok() and Expr()) and (printBool("*****bool print token... " + str(tok.value)) and tok.value == const.RPAREN):
            printBool("returning true.....")
            updateTok()
            if tok.value == const.SEMICOLON:
                return True
            else:
                return  updateTok() and Expr()
    """



"""
    else:
        printBool("going to Expr from here")
        return (Expr() and  tok.value == const.SEMICOLON) and (updateTok() and Stmt())

    """
