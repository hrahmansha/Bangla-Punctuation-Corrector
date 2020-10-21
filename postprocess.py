import sys

puncMapp = [",COMMA", "?QUESTIONMARK", "।PERIOD", "!EXCLAMATIONMARK"]

quesWord = ["কি","কেন","কী","কোথায়","কে","নাকি","পারি","তুমি","চাও","পারবে","করছ","তাইনা","চান","আছো","করেন"]
commaWord = ["যে","হ্যাঁ","ওহ","করি","হ্যা","করা","তো","বলেন","গেছে","বলেছেন","আচ্ছা","হয়েছে","স্যার","করবে","এখন"]
periodWord = ["না","হবে","হয়েছে","হয়","পারে","নেই","হচ্ছে","ছিল","যায়","নয়","থাকে","রয়েছে","জন্য","যাচ্ছে","যাবে"]
exclamWord = ["যাও","করো","দাও","কর","চলো","থামো","করুন","হেই","আসো","বাবা","জলদি","খোদা","হও","থাকো","মা"]

def postProcess(input, output, queslimit, commalimit, periodlimit, exclamlimit):
    with open(input, "r") as myfile:
        lines = myfile.readlines()
        
        out = open(output, "w")
        out.write("")
        for line in lines:
            words = line.split()
            length = len(words)
            text = ""
            for i in range(length):
                word = words[i]
                text += word+" "
                if word in quesWord[:queslimit]:
                    if i == (length-1):
                        text += "?QUESTIONMARK "
                    elif words[i+1] in puncMapp:
                        words[i+1] = "?QUESTIONMARK"
                    else :
                        text += "?QUESTIONMARK "
                elif word in commaWord[:commalimit]:
                    if i == (length-1):
                        text += ",COMMA "
                    elif words[i+1] in puncMapp:
                        words[i+1] = ",COMMA"
                    else :
                        text += ",COMMA "
                elif word in periodWord[:periodlimit]:
                    if i == (length-1):
                        text += "।PERIOD "
                    elif words[i+1] in puncMapp:
                        words[i+1] = "।PERIOD"
                    else :
                        text += "।PERIOD "
                elif word in exclamWord[:exclamlimit]:
                    if i == (length-1):
                        text += "!EXCLAMATIONMARK "
                    elif words[i+1] in puncMapp:
                        words[i+1] = "!EXCLAMATIONMARK"
                    else :
                        text += "!EXCLAMATIONMARK "
                    
            # print(text) 
            text += "\n"
            out = open(output, "a")
            out.writelines(text)
            out.close()   

                # print(word)
            # print(line)
            # print(words)
if __name__ == "__main__":

    if len(sys.argv) > 1:
        input_path = sys.argv[1]
    else:
        sys.exit("Input file path argument missing")

    if len(sys.argv) > 2:
        output_path = sys.argv[2]
    else:
        sys.exit("Postprocessed output file path argument missing")

    maxQues = int(sys.argv[3])
    maxComma = int(sys.argv[4])
    maxPeriod = int(sys.argv[5])
    maxExclam = int(sys.argv[6])

    print("input path:"+input_path)
    print("output path:"+output_path)
    print("# of Q words:"+str(maxQues))
    #print(type(maxQues))
    print("# of C words:"+str(maxComma))
    print("# of P words:"+str(maxPeriod))
    print("# of E words:"+str(maxExclam))

    postProcess(input_path, output_path, maxQues, maxComma, maxPeriod, maxExclam)

    # compute_error([target_path], [predicted_path])  
