import sys
import const
import lexanalysis
from collections import deque 
  



tok = lexanalysis.getNextToken()
stack = deque() 


print(tok)
def updateTok():
    #print("printing from updatetok OXOXOXOXOXOXXOOXOXOXO")
    global tok
    tok = lexanalysis.getNextToken()
    print(tok)
    if tok != None:
        return True
    else:
        return False

def reportError(tok):
    print("*** Error line ", tok.lineno, ".")
    print(lexanalysis.lines[tok.lineno - 1])
    print("*** syntax error")
    pass


def getStackTop():
    global stack
    top = stack.pop()
    stack.append(top)
    return top

def Program():
    if tok == None:
        return False
    print("inside program")
    return Decl() and ProgramP()


def ProgramP():
    updateTok()
    if tok != None:

        return Program()
    else: 
        print("ending")
        return True



def Decl():
    print("inside decl")
    print(tok.value)
    if tok.value in const.typeList or tok.value == const.VOID:
        print("method type  found")
        updateTok()
        if tok.type == "T_Identifier":
            updateTok()
            print("tok.value", tok.value)
            if tok.value ==  const.LPAREN:
                return FunctionDecl()
            else:
                print("going to vardecl") 
                return VariableDecl()

    

def VariableDecl():
    print("inside var decl")
    if tok.value == const.SEMICOLON:
        print("semicolon found after var")
        return True
    else:
        reportError(tok)


def FunctionDecl():
    print("inside funcdecl")
    updateTok()
    forms  = Formals()
    
    updateTok()
    return forms  and StmtBlock()


def Formals():
    print("inside formals")
    if tok.value == const.RPAREN:
        return True
    elif tok.value in const.typeList:
        print("typelist found")
        updateTok()
        if tok.type == const.IDENT:
            updateTok()
            if tok.value == const.COMMA and (updateTok() and tok.value != const.RPAREN):
                return updateTok() and Formals()
            
            elif tok.value == const.RPAREN:
                print("returning from formals")
                return True
        else:
            reportError(tok)
    
def StmtBlock():
    print("inside stmtBlock")
    if tok.value == const.LCURLEY:
        updateTok()
        if tok.value == const.RCURLEY:
            return True
        else:
            stmtBlckVar = VariableDeclRec() and printBool("token inside stmtBlock " + tok.value) and  tok.value == const.RCURLEY
            updateTok()
            return stmtBlckVar
                

        """
        elif tok.value in const.typeList:
            return VariableDeclRec()
        else:
            Stmt()
        """
def VariableDeclRec():
    print("inside varDecRec")
    #if tok.value == const.RCURLEY:
    #        return True
    if tok.value in const.typeList and (updateTok() and tok.type == const.IDENT):
        updateTok()
        return VariableDecl() and (updateTok() and VariableDeclRec()) 
    else:
        print("going to statement........................")
        #return Stmt()
        while True:
            print("inside while loop VarDeclRec !!!!!!!!!!!!!!!!!")
            if Stmt(): 
                if tok.value == const.RCURLEY:
                    print("returning true from VarDeclRec")
                    return True
                if tok.value == const.ELSE:
                    print("else found")
                    return True
                updateTok()
                
                pass
            else:
                return True
                


def Stmt():
    
    print("inside stmt tok value", tok)
    if tok.value == const.RCURLEY:
        print("returning after RCURLEY")
        return True

    #comment out due to debbuging
    #updateTok()
    if tok.value == const.IF:
        print("&&&&&& sending to if")
        if updateTok() and IfStmt():
            #updateTok()
            if tok.value == const.RCURLEY:
                print("RCURLEY found after ifSTMT......")
                return True
            else:
                return  Stmt()
    
    elif tok.value == const.WHILE:
        if updateTok() and WhileStmt():
            if tok.value == const.RCURLEY:
                print("RCURLEY found after WHILE_STMT......")
                return True
            else:
                print("STMT found instead of RCURLEY")
                return Stmt()


    elif tok.value == const.FOR:
        return updateTok() and ForStmt() and updateTok() and Stmt()

    #might need to add sth
    elif tok.value == const.BREAK:
        return updateTok() and BreakStmt() and updateTok() and Stmt()

    elif tok.value == const.RETURN:
        print("return found..............")
        return updateTok() and ReturnStmt()
    
    elif tok.value == const.PRINT: #and (updateTok() and tok.value == const.LPAREN):
        return updateTok() and PrintStmt() and updateTok() and Stmt()

    elif tok.value == const.SEMICOLON:
        print("semicolon found")
        return True

    elif tok.value == const.LCURLEY:
        
        return StmtBlock() and printBool("returning from stmtBlock() " + tok.value)
    
    elif Expr() and tok.value == const.SEMICOLON:
        print("returning after getting expr() and semicolon")
        return True
        """
        print("return from stmt()")
        boolVar = Expr() and tok.value == const.SEMICOLON and updateTok()
        if boolVar == True and tok.value == const.ELSE:
            return True
        else:
            return Stmt()
        """
    
        #on getting "{", code for stmt-->stmtBlock


def printBool(st):
    print(st)
    return True
"""
Expr ::= LValue = Expr | Constant | LValue | Call | ( Expr ) |
    Expr + Expr | Expr - Expr | Expr * Expr | Expr / Expr |
    Expr % Expr | - Expr | Expr < Expr | Expr <= Expr |
    Expr > Expr | Expr >= Expr | Expr == Expr | Expr ! = Expr |
    Expr && Expr | Expr || Expr | ! Expr | ReadInteger ( ) |
    ReadLine ( )
"""
def Expr():
    print("inside Expr")
    print(tok)

    #changed today
    """if tok.value == const.READINT:
        return True
    
    elif tok.value == const.READLINE:
        return True
    """

    if tok.value == const.LPAREN:
        print("((((((( leftParen found")
        #new code added and next token removed from if
        if (updateTok() and Expr()) and (printBool("*****bool print token... " + str(tok.value)) and tok.value == const.RPAREN):
            print("returning true.....")
            updateTok()
            if tok.value in const.operatorList:
                print("operator list found in lparen")
                return  updateTok() and Expr()
            else:
                return True
    


    elif tok.value == const.MINUS:
        return (updateTok() and Expr())

    elif tok.value == const.NOT:
        return updateTok() and Expr()
    
    elif tok.type == const.IDENT:
        print("var ", tok.value, "found")
        updateTok()
        print("checkpoint ...2 ")
        if tok.value == const.LPAREN:
            print("checkpoint ... 3")
            updateTok()
            return Actuals()
        
        elif (tok.value == const.EQUAL) or (tok.value in const.operatorList):
            print("equal found")
            return updateTok() and Expr()
        else: 
            
            return True
        
        #elif tok.value in const.operatorList:
        #    return updateTok() and Expr()
            
    elif tok.type in const.constantList:
        print("constant found")
        updateTok()
        if tok.value in const.operatorList:
            print("operator found after constant")
            return updateTok() and Expr()
        else:
            #changed from return true to return Expr()
            return True
    
    
    #ReadInteger ( )
    elif tok.value == const.READINT or tok.value == const.READLINE:
        print("readline or readint found............................")
        if (updateTok() and tok.value == const.LPAREN) and (updateTok() and tok.value == const.RPAREN):
            updateTok()
            return True
    else:
        print("some error")
        return False


def Actuals():
    print("inside actuals")
    if tok.value == const.RPAREN:
        return True
    
    updateTok()
    if not Expr():
        return False
    updateTok()
    if tok.value == const.COMMA and (updateTok() and tok.value != const.RPAREN):
        return updateTok() and Actuals()
    
    elif tok.value == const.RPAREN:
        return True


    
def IfStmt():
    print("inside ifStmt")
    if tok.value == const.LPAREN:
        ifVar = (updateTok() and Expr()) and (printBool("if ..." + str(tok.value)) and  tok.value == const.RPAREN)
        if not ifVar:
            print("error inside if")
            return False
        if updateTok() and (printBool("calling stmt() from if")) and not Stmt():
            print("ret false from ifStmt")
            return False
        print("-----------", tok)
        if tok.value == const.SEMICOLON:
            updateTok()
        
        
            
        if  tok != None and tok.value == const.ELSE:
            print("else found!!!")
            updateTok()
            if not Stmt():
                print("returning false from else*****")
                return False 
            else:
                print("true for if with else------------------------------------", tok)
                return True
        else:
            print("true for if-----------XXXX-------------------------", tok)
            return True
    else:
        reportError(tok)
        return False


def ForStmt():
    print("inside FOR STMT___________________________---")
    if tok.value == const.LPAREN:
        #semicolon found for( ;  )
        print("lparen found")
        if updateTok() and tok.value == const.SEMICOLON:
            print("First expresion not found")
            pass
        # for(i = 1;)
        elif not Expr() or (updateTok() and tok.value != const.SEMICOLON):
            print("second part is returning false")
            return False

        # for( i = 1; i > 5;)
        print("token...", tok)
        updateTok()
        if not Expr() or  (printBool("inside if~~~~~~~" + tok.value) and  not tok.value == const.SEMICOLON):
            print("third part also returning false")
            return False 
        # for( i = 1; i > 5; )
        updateTok()
        print("entering final part tok = ", tok)
        if tok.value == const.RPAREN:
            print("----------returning true from  without third part")
            return updateTok() and Stmt()

        elif Expr() and printBool("from third part......" + tok.value) and tok.value == const.RPAREN:
            print("++++++returning true from  with third part")
            return updateTok() and Stmt()
        
def WhileStmt():
    if tok.value == const.LPAREN:
        
        whileVar = (updateTok() and Expr()) and (printBool("while!!!!!!!!!!!!!" + str(tok.value)) and tok.value == const.RPAREN)
        if not whileVar:
            print("error inside while.....")
            return False
        
        if updateTok() and not Stmt():
            print("false in while O_O_O_O_O_O_O_O_")
            return False           
        print("true for while....", tok)
        return True
    else:
        return False


def ReturnStmt():
    print("inside return stmt()", tok)
    if tok.value == const.SEMICOLON:
        return True
    elif Expr()  and (tok.value == const.SEMICOLON) and updateTok():
        return True
    else:
        return False

def BreakStmt():
    if tok.value == const.SEMICOLON:
        print("inside breakstmt() ", tok)
        return True

#PrintStmt  --> Print ( Expr + , ) ;
#input Print(a, " ");
def PrintStmt():
    #LPRAREN checking removed from the caller method  
    print("PPPPPPPPPP>>..>>>>>>>>inside print stmt", tok)
    if  tok.value == const.LPAREN: 
        while True:
            print("inside print loop")
            updateTok()
            if not Expr():
                print("returning false from printStmt")
                return False
            if tok.value == const.COMMA:
                print(",,,,,,,,,,,,, comma found")
                #updateTok()
                continue
            elif tok.value == const.RPAREN:
                print("Rparenn found ........in print ")
                updateTok()
                print(tok)
                if  tok != None and tok.value == const.SEMICOLON:
                    print("returning true")
                    return True
                else:
                    print("returning false")
                    return False
            
    else:
        return False
    
        
    

def main():
    print(Program())
    #    print("true")

if __name__ == "__main__":
    main()





###########""""""""""
"""
   
    elif tok.value == const.LPAREN:
        print("((((((( leftParen found")
        #new code added and next token removed from if
        if (updateTok() and Expr()) and (printBool("*****bool print token... " + str(tok.value)) and tok.value == const.RPAREN):
            print("returning true.....")
            updateTok()
            if tok.value == const.SEMICOLON:
                return True
            else:
                return  updateTok() and Expr()
    """



"""
    else:
        print("going to Expr from here")
        return (Expr() and  tok.value == const.SEMICOLON) and (updateTok() and Stmt())

    """
