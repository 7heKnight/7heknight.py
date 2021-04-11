import re

# ======================== CHECK EXIST FILE ========================
def isExist(fileName):
    try:
        with open(fileName):
            return True
    except:
        return False

# ==================== Get Sent email into list ====================
def getEmails(fileName):
    openFile = open(fileName)
    text = openFile.read()
    listSender = re.findall('From (\S+?)[ ]', text)
    if len(listSender) == 0:
        exit('[-] None emails found.')
    return listSender

# ======================= Get each email sent =======================
def mailList(emails):
    sender = []
    for senderPos in emails:
        if senderPos not in sender:
            sender.append(senderPos)
    return sender, emails

# ================= Count times of each email sent ==================
def timesSent(sender, listSender):
    times = {i : 0 for i in sender}
    for i in listSender:
        times[i] += 1
    return times

# ====================== Get common emails sent ======================
def mostSent(times, sender):
    maxSent = times[max(times)]
    common_email = []
    for i in sender:
        if times[i] == maxSent:
            common_email.append(i)
    return common_email, maxSent

# =============================== Main ===============================
if __name__=='__main__':
    filename = 'mail.txt'
    if not isExist(filename):
        exit('[-] File not found!')
    sender, listSender = mailList(getEmails(filename))
    timeSent = timesSent(sender, listSender)
    common_email, times = mostSent(timeSent, sender)
    print(f'[+] Most sending is: {times} times with belowing email:')
    for i in common_email:
        print(f'   - {i}')
