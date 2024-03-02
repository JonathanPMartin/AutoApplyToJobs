import requests
import json
import webbrowser
import random
from pynput.keyboard import Key, Controller
from pynput.keyboard import Listener, KeyCode
from pynput.mouse import Button
from pynput.mouse import Controller as controller
from pynput import keyboard
import time
#file= open("AutomaticJobs.txt", "a")
#file= open("NonAutomaticJobs.txt", "a")
#file= open("NonAutomaticCurJob.txt", "a")
#file=open('CenterAutomaticJobs.txt','a')
#file=open('CenterCurAutomaticJobs.txt','a')
#file=open('RightAutomaticJobs.txt','a')
#file=open('RightCurAutomaticJobs.txt','a')


#file.close()

#file=open('flag.txt','a')
#file.close()
file=open('flag.txt','r')
#print(json.loads(file.read()).keys())
flaged={'software+devloper':0}
#print(json.dumps(flaged))
file.close()


def findNewJobs(job,location,distance):#grabs jobs from reed and returns them in a list
    link='https://www.reed.co.uk/api/1.0/search?keywords='+job+'&locationName='+location+'&distanceFromLocation='+distance
    response = requests.get(link,auth=("619f5ac8-2fbd-4a77-86b9-bb3facc3a793",""))
    start_filter=response.json()
    start_filter=start_filter['results']
    Urls=[]
    baseurls=[]
    for loop in start_filter:
        #print(loop['jobDescription'])
        Urls.append(loop['jobUrl'])
        tem=loop['jobUrl'].split('jobs/')[1]
        tem2=tem.split('/')
        if tem2 in baseurls:
            useless=0
        else:
            baseurls.append(tem2[0])
        #print(tem2[0])
        #print(loop['jobUrl'])
    return Urls

def CheckForOverlap(Urls,fileNmae): #checks if the jobs returned from find new jobs already exist in the txt file
    file= open(fileNmae, "r")
    toappend=[]
    curUrls=file.readlines()
    for i in Urls:
        test=i+'\n'
        print(test in curUrls)
        if test in curUrls:
            print('OverLap')
            usless=0
        else:
            toappend.append(i)
    file.close()
    file=open(fileNmae, "a")
    for i in toappend:
        tem=i+'\n'
        file.write(tem)
    file.close()
    
def AddFlag(BaseUrl): #flaging system used to determine if a url's origin can be trusted
    file=open('flag.txt','r')
    flags=json.loads(file.read())
    dickeys=flags.keys()
    num=1
    if BaseUrl in dickeys:
        num=num+flags[BaseUrl]

    if num>9:
        newfile=open('flaged.txt','a')
        newfile.write(BaseUrl+'\n')
    flags[BaseUrl]=num
    text=json.dumps(flags)
    file.close()
    file=open('flag.txt','w')
    file.write(text)
    file.close()

#apply-options-top
    
def BulkJobSearch(Location,Distance): #does what it says on the tin
    jobs=['software+devloper','python','PHP','javascript','it+consultant','Cloud+engineer','dev+ops','sql','security+engineer','Software+developer','Web+developer','Front-end+developer','Mobile+app+developer']
    terms=['graduate','junior','intern','internship','apprentice','apprenticeship','trainee']
    JobUrls=[]
    for i in jobs:
        for j in terms:
            full_job=j+'+'+i
            for k in findNewJobs(full_job,Location,Distance):
               JobUrls.append(k)
               print('...Loading...')
    CheckForOverlap(JobUrls,'Jobs.txt')
    FilterJobs(JobUrls)
    print('done!')
def ApplyingtoJobs():
    loop=True
    file= open("CurJob.txt", "r")
    curJob=int(file.read())
    file.close()

        
    while loop:
        file=open('flaged.txt','r')
        flaggedurls=file.readlines()
        file.close()
        test=True
        file= open("Jobs.txt", "r")
        curUrl=file.readlines()[curJob]
        file.close()
        for i in flaggedurls:
            if i in curUrl:
                test=False
        if test:
            webbrowser.open(curUrl) 
            print(curUrl)
        else:
            print('the last URL has been flagged')
        UserInput=int(input('1)flag the last url and move on \n2)move on to the next job \n3)finish\n:'))
        if UserInput==1:
             flag=curUrl.split('/')
             flag=flag[0]
             AddFlag(flag)
             curJob=curJob+1
        elif UserInput==2:
            curJob=curJob+1
        elif UserInput==3:
            file=open('CurJob.txt','w')
            file.write(str(curJob))
            file.close()
            loop=False
        else:
            print('please input 1,2 or 3')
        



def ApplyingAutoJobsSpef(RightOrCenter):
    loop=True
    tempFileName=RightOrCenter+'CurAutomaticJobs.txt'
    temFileName2=RightOrCenter+'AutomaticJobs.txt'
    file= open(tempFileName, "r")
    curJob=int(file.read())
    file.close()

        
    while loop:
        file=open('flaged.txt','r')
        flaggedurls=file.readlines()
        flags=[]
        for flag in flaggedurls:
            Realflag=flag.split('\n')[0]
            flags.append(Realflag)
        file.close()
        test=True
        file= open(temFileName2, "r")
        lines=file.readlines()
        curUrl=lines[curJob]
        print(curJob)
        print(len(lines))
        file.close()
        for i in flags:
            if i in curUrl:
                print(i)
                test=False
        if curUrl=='\n':
            test=False
        if test:
            webbrowser.open(curUrl) 
            print(curUrl)
            time.sleep(12)
            mouse = controller()
            #mouse.position = (960, 465)
            mouse.press(Button.left)
            mouse.release(Button.left)
            temkeyboard = Controller()
            time.sleep(7)
            with temkeyboard.pressed(Key.ctrl):
                temkeyboard.press('w')
                temkeyboard.release('w')
        else:
            useless=0
        curJob=curJob+1
        if curJob==len(lines):
            curJob=curJob-1
            curJob=str(curJob)
            temFile=open(tempFileName, "w")
            temFile.write(curJob)
            loop=False

def FilterJobs(Urls):#detects if a job can be fully automated or not
    CenterApply=[]
    RightApply=[] 
    AutoJobs=[]
    NonAutojobs=[]
    for Url in Urls:
        Loading='...Loading...'+str(random.randint(0,100))
        print(Loading)
        curUrl=Url.split('\n')[0]
        Request=requests.get(curUrl)
        Body=str(Request.content)
        Automatic="Easy Apply" in Body
        if Automatic:
            if 'apply-options-top' in Body:
                CenterApply.append(Url)
                print('IT WORKED')
            elif'apply-options' in Body:
                 RightApply.append(Url)
                 print('IT WORKED')
            else:
                print('Job No Longer Exits')
            
        elif 'The following job is no longer available' in Body:
            print('Job no longer exists')
        else:
            
            if 'Apply now' in Body:
                print('not automatic')
                NonAutojobs.append(Url)
            else:
                print('not a job')

    #print(AutoJobs)    
    CheckForOverlap(CenterApply,'CenterAutomaticJobs.txt')
    CheckForOverlap(RightApply,'RightAutomaticJobs.txt')
    #CheckForOverlap(AutoJobs,'AutomaticJobs.txt')
    CheckForOverlap(NonAutojobs,'NonAutomaticJobs.txt')
    #file= open("AutomaticJobs", "a")
    #print(type(AutoJobs))
    
def Options():
    loop=True
    while loop:
        Userinput=int(input('1)Job Search\n2)Aplying to jobs\n3)done\n:'))
        if Userinput==1:
            Location=input('what location do you want to apply(Note London is what you normally do) \n:')
            Distance=input('in miles how far are you willing to travel from this location? \n:')
            BulkJobSearch(Location,Distance)
        elif  Userinput==2:
            ApplyingAutoJobsSpef('Center')
        elif Userinput==3:
            loop=False
        else:
            print('please input 1,2 or 3')
    
#FilterJobs()
file=open('AutomaticJobs.txt','r')
Url=file.readlines()
#FilterJobs(Url)
Options()
#ApplyingAutoJobsSpef('Right')
#ApplyingAutoJobsSpef('Center')
Locations=['London','Coventry','birmingham']
distance=1
while True:
    for i in Locations:
        BulkJobSearch(i,str(distance))
    distance=distance+1
    ApplyingAutoJobsSpef('Right')
#['junior-desk-analyst-python-hedge-fund', 'graduate-software-engineer-developer-python-c-c-java', 'senior-programme-manager', 'graduate-junior-engineer', 'graduate-software-engineer', 'graduate-technical-analyst', 'graduate-devops-engineer', 'graduate-junior-developer-python-javascript-php-london', 'graduate-software-developer', 'graduate-junior-developer-python-linux-c-java-london', 'it-engineering-graduate', 'graduate-sales-data-analyst', 'product-specialist-graduate-level', 'graduate-software-engineer-multiple-roles', 'technical-support-engineer-graduate-considered', 'c-net-developer', 'junior-java-developer', 'junior-developer', 'trainee-junior-it-contract-recruitment-consultant-it-development', 'quantitative-developer', 'sales-data-analyst-assistant', 'senior-front-end-developer-fully-remote', 'irb-manager', 'junior-software-tools-platform-engineer-guildford-40k', 'machine-learning-research-engineer', 'thermal-engineer', 'graduate-junior-valuations-equity-derivatives-tier-1-bank', 'junior-python-developer', 'python-developer', 'senior-python-engineer', 'senior-python-full-stack-engineer', 'software-developer-python-django', 'junior-energy-trader', 'junior-software-engineer', 'junior-data-scientist', 'junior-penetration-tester', 'junior-test-engineer', 'junior-test-analyst', 'junior-platform-engineer', 'junior-devops-engineer', 'coding-and-programming-trainee', 'data-analyst-trainee', 'junior-mid-java-developer', 'devops-engineer-sre-aws-junior-mid', 'senior-data-analyst-hybrid-6-12-months-heathrow', 'data-engineer-crypto-infrastructure', 'pensions-data-migration-analyst', 'senior-software-engineer-backend-focus', 'senior-data-engineer-role', 'senior-data-engineer', 'senior-devops-engineer-uk-nationals-only', 'ai-research-intern', 'machine-learning-speech--paid-internship', 'rev-celerator-internship-programme-data-analyst', 'rev-celerator-internship-programme-information-security-analyst-operations', 'data-engineering-apprentice', 'devops-engineer-apprentice', 'global-markets-data-science-apprenticeship-2024-london', 'trainee-web-developer', 'junior-php-developer', 'senior-php-developer', 'senior-php-web-developer', 'php-developer-hybrid-london', 'junior-website-developer', 'full-stack-developer-php-laravel-javascript-london', 'lead-drupal-developer', 'software-developers-react-javascript-c-net-wanted', 'graduate-net-developer-london', 'net-developer-graduate-junior-computer-gaming-co-london', 'software-engineers-x-5-react-java-javascript-net', 'lead-javascript-developer-ecommerce', 'senior-front-end-developer-javascript-vuejs', 'junior-sales-executive', 'junior-software-developer', 'junior-web-developer-intern', 'senior-developer-c-net', 'junior-net-developer-online-film-rental-company-london', 'senior-software-engineer', 'umbraco-developer-up-to-45000', 'senior-apex-developer', 'senior-full-stack-engineer', 'senior-software-developer', 'senior-full-stack-developer', 'frontend-mobile-engineer', 'lead-react-native-mobile-engineer', 'servicenow-architect-itom-cmdb-discovery-to-85k', 'r-d-tax-assistant-manager', 'sr-d365-ce-developer', 'senior-technical-support-engineer', 'software-developer', 'ppc-am', 'net-developer', 'senior-software-engineer-backend', 'net-software-developer', 'python-developer-software-engineer-aws-finance-trading-london', 'senior-python-software-engineer-developer-finance-london', 'graduate-recruitment-consultant', 'trainee-graduate-recruitment-consultant', 'psychology-graduate', 'graduate-consultant', 'recruitment-consultant', 'graduate-teaching-assistant', 'graduate-aspiring-psychologists', 'trainee-recruitment-consultant', 'tech-recruitment-consultant', 'psychology-graduate-teaching-assistant', 'graduate-consultant-programme', 'graduate-marketing-consultant', 'graduate-consultant-scheme', 'graduate-sales-consultant', 'graduate-it-support-technician', 'recruitment-consultant-sales-experience-required', 'senior-recruitment-consultant-quant-finance', 'trainee-recruitment-consultant-salespeople-wanted', 'senior-recruitment-consultant-tech-finance-tax-legal', 'graduate-recruitment-consultant-graduate-scheme', 'trainee-recruitment-consultant-legal-and-governance', 'senior-principal-recruitment-consultant-corporate-finance', 'recruitment-consultant-cleantech-sustainability-energy', 'graduate-trainee-recruitment-consultant', 'graduate-consultant-french-speaker', 'graduate-consultant-german-speaker', 'graduate-consultant-swedish-speaker', 'trainee-recruitment-consultant-estate-agents-salespeople-wanted', 'associate-recruitment-consultant-accountancy-finance-asap-start', 'graduate-recruitment-consultant-relocation', 'graduate-eia-consultant-london', 'graduate-recruitment-consultant-chessington', 'graduate-consultant-programme-french-speaker', 'graduate-consultant-programme-german-speaker', 'junior-consultant', 'junior-cdm-consultant', 'junior-recruitment-consultant', 'junior-consultant-programme', 'junior-technical-consultant', 'junior-marketing-consultant', 'junior-management-consultant', 'junior-recruiter-cross-train-from-sales', 'junior-sales-executive-cross-train-to-recruitment', 'junior-legal-recruitment-consultant', 'recruitment-resourcer-junior-consultant', 'junior-headhunter', 'junior-recruitment-consultant-no-experience-needed', 'junior-principal-designer', 'junior-category-manager', 'junior-office-manager', 'junior-product-manager', 'it-project-consultant-data-analyst-cloud', 'junior-sales-manager', 'junior-technology-recruiter', 'acoustic-consultant', 'junior-sales-development-representative', 'junior-sales-development-manager', 'junior-customer-service-representative', 'junior-business-development-associate', 'senior-geoenvironmental-consultant', 'servicenow-technical-consultant', 'senior-acoustics-consultant', 'senior-dc-investment-pensions-consultant', 'recruitment-consultant-life-sciences-exp-needed', 'r-d-tax-credits-consultant-senior-associate', 'db-pensions-administration-consultant-team-manager-home-flexible-working-options', 'evaluator-senior-consultant-ad-energy-environment', 'assistant-accountant', 'senior-db-pensions-administrator-home-flexible-working-options', 'associate-pension-consultants-senior-administrators-team-leaders', 'senior-ecologist', 'pension-administration-consultants-team-leader', 'sous-chef-private-members-club-monday-to-friday', 'account-manager-destination-pr', 'marketing-manager-healthcare-wellness-clinic', 'regional-specification-sales-manager-iot-social-housing', 'private-client-solicitor-nq-3', 'senior-architect', 'senior-strategist-london', 'paid-media-account-director', 'head-chef', 'paid-media-manager', 'senior-corporate-actions-administrator', 'tax-advisor', 'commercial-account-handler', 'primary-cover-teacher', 'supply-teacher', 'supply-primary-teacher', 'senior-cloud-engineers-x-3-azure-devops-terraform-ci-cd', 'presales-consultant', 'corporate-responsibility-intern-london-12-month-placement-2024-2025', 'recruitment', 'it-lecturer', 'apprentice-office-assistant', 'learning-development-coach-retail-southampton', 'vehicle-technician', 'impact-academy-trainee-education-recruitment-consultant', 'trainee-energy-consultant', 'trainee-management-consultant', 'trainee-sales-consultant', 'trainee-recruitment-consultant-researcher', 'trainee-recruitment-consultant-entry-level', 'trainee-recruitment-consultant-rec2rec', 'it-technician', 'trainee-recruitment-consultant-relocation-opportunity', 'trainee-recruitment-consultant-sales-background', 'trainee-recruitment-consultant-graduates-wanted', 'trainee-recruitment-consultant-training-programme', 'trainee-recruitment-consultant-central-london', 'trainee-recruitment-consultant-rolex-incentive', 'entry-level-trainee-recruitment-consultant', 'trainee-recruitment-consultant-immediate-start', 'trainee-recruitment-consultant-no-experience', 'trainee-graduate-recruitment-consultant-finance', 'trainee-marketing-recruitment-consultant-sales', 'trainee-recruitment-consultant-relocation-to-us', 'trainee-recruitment-consultant-no-experience-required', 'no-experience-needed-trainee-recruitment-consultant', 'trainee-recruitment-consultant-high-earning-potential', 'trainee-headhunter', 'broadcast-operational-support-engineer', 'cloud-infrastructure-engineer', 'senior-software-developer-engineer', 'junior-media-systems-engineer', 'senior-aws-infrastructure-engineer-cloud-solutions-architect', 'junior-devops-engineer-mid-level-devops-engineer', 'senior-aws-cloud-infrastructure-engineer-gatwick-hybrid', 'devops-engineer', 'windows-engineer', 'firmware-electronics-engineer', 'lead-data-engineer', '3rd-line-engineer', 'senior-java-kotlin-engineer', 'senior-application-engineer-imanage', 'senior-aws-platform-engineer', 'infrastructure-engineer-jan-2024', 'senior-electronics-engineer', '2nd-line-support-engineer', 'data-engineering-trainer', 'data-architect-110k-bonus-stocks-option', 'senior-sdet', 'lead-sdet', 'senior-devops-engineer', 'senior-software-engineer-data-business-intelligence', 't3-implementation-engineer', 'helpdesk-engineer', '3rd-line-it-support-field-projects-engineer-east-sussex-uk', 'helpdesk-leader-supervisor', 'cyber-security-trainee', 'd365-f-o-lead-developer', 'graduate-data-administrator', 'junior-systems-analyst', 'junior-sql-developer', 'junior-sql-developer-ecommerce-company', 'infrastructure-engineer-junior', 'junior-data-engineer', 'data-analyst-junior', 'junior-analyst-developer', 'software-engineer-team-lead', 'lead-software-engineer', 'junior-mi-data-analyst', 'junior-pensions-data-consultant', 'junior-d365-bc-developer-45000', 'junior-mid-level-server-engineer', 'power-bi-analyst', 'senior-software-engineer-remote-c60k', 'head-of-data-science', 'pricing-manager', 'group-finance-systems-manager', 'quantitative-developer-pricing-derivatives-sell-side-or-buy-side', 'lead-credit-risk-strategy-analyst', 'senior-exposure-management-analyst', 'senior-risk-analyst-lng-trading', 'digital-audit-tech-fs-senior-associate', 'senior-pricing-analyst', 'financial-modelling-manager', '2nd-line-it-infrastructure-engineer', 'credit-risk-analyst', 'digital-audit-manager-fs', 'senior-desktop-engineer', 'software-developer-apprentice', 'data-analyst', 'ot-cyber-engineer', 'it-support-engineer', 'field-service-engineer', 'first-line-technical-support-engineer', 'it-support', 'junior-fire-and-security-engineer', 'security-engineer', 'security-installation-engineer', 'junior-field-engineer', 'security-systems-engineer', 'junior-bms-engineer', 'junior-installation-service-engineer-fire-and-security', 'junior-infrastructure-engineer', 'firmware-engineer', 'fire-and-security-engineer', 'senior-network-and-security-engineer', 'junior-it-support-engineer', 'junior-fire-alarm-engineer-extinguisher-engineer-training-provided', 'security-systems-engineer-access-control-cctv-intruder-alarms', 'geotechnical-engineer', 'electricians-mate-junior-door-entry-installation-engineer', 'trainee-bms-engineer', 'gate-automation-engineer', 'senior-development-engineer', 'industrial-door-engineer', 'fire-alarm-service-engineer', 'automatic-gate-engineer', 'field-service-engineer-bms', 'senior-embedded-software-engineer', 'it-service-desk-engineer', '3rd-line-service-desk-engineer', 'automatic-gate-barrier-engineer', 'dv-cleared-data-architect', 'network-architect', 'it-support-3rd-line-fire-engineering', 'it-support-fire-engineering', 'apprentice-trainee-garage-door-engineer', 'machine-operator', 'mechanical-fitter', 'reactive-and-extra-works-supervisor', 'manufacturing-engineer', 'electrical-engineer', 'multiskilled-maintenance-engineer', 'lead-shift-engineer', 'multiskilled-shift-maintenance-engineer', 'fire-pump-service-engineer', 'audio-visual-senior-onsite-av-engineer', 'project-engineer-id162476', 'service-technician-temporary-mobile-cctv-towers', 'trainee-fire-extinguisher-engineer-ref23408', 'trainee-engineer', 'trainee-cyber-security-analyst', 'lead-gas-engineer-nco2', 'trainee-lightning-protection-engineer', 'trainee-it-security-analyst-no-experience-required', 'assistant-field-engineer-driver-trainee', 'junior-data-developer', 'junior-automation-developer', 'c-developer', 'java-developer', 'lead-mendix-developer', 'salesforce-developer-experience-cloud-outside-ir35', 'unity-c-engineer-3-month-initial-contract-250-300-outside-ir35-remote', 'senior-civil-engineer', 'salesforce-developer', 'netsuite-developer', 'senior-java-developer-fixed-income-trading-vp-d', 'senior-aws-developer', 'python-developer-fintech', 'driving-instructor-trainee', 'trainee-driving-instructor']



