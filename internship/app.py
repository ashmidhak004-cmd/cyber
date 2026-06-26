from flask import Flask, render_template, abort

app = Flask(__name__)

# Categories metadata
CATEGORIES = {
    'financial': {
        'title': '💰 Financial Crimes',
        'desc': 'Learn how to protect your money from digital pocket-pickers.',
        'class': 'color-fin'
    },
    'social': {
        'title': '📱 Social Media Crimes',
        'desc': 'Learn how to safeguard your personal accounts and verify friend requests.',
        'class': 'color-soc'
    },
    'hacking': {
        'title': '💻 Hacking & Technical Attacks',
        'desc': 'Learn how to detect browser hijackers and protect your connections.',
        'class': 'color-hac'
    },
    'misc': {
        'title': '⚠️ Miscellaneous Crimes',
        'desc': 'Detect hidden job traps and voice scams that target families.',
        'class': 'color-misc'
    }
}

# Scenario to category mapping and next link configuration
SCENARIOS = {
    'sms-lottery': {'category': 'financial', 'next': 'email-bank'},
    'email-bank': {'category': 'financial', 'next': 'wa-friend'},
    'wa-friend': {'category': 'social', 'next': 'dm-copyright'},
    'dm-copyright': {'category': 'social', 'next': 'scareware'},
    'scareware': {'category': 'hacking', 'next': 'wifi-snare'},
    'wifi-snare': {'category': 'hacking', 'next': 'job-scam'},
    'job-scam': {'category': 'misc', 'next': 'grandparent-call'},
    'grandparent-call': {'category': 'misc', 'next': None}
}

# Category to list of scenarios mapping
CATEGORY_SCENARIOS = {
    'financial': [
        {'id': 'sms-lottery', 'title': 'The Jackpot SMS', 'desc': 'Spot warning signs in prize text alerts.', 'icon': 'fa-solid fa-message'},
        {'id': 'email-bank', 'title': 'The Suspicious Email', 'desc': 'Learn how bank credential scams look.', 'icon': 'fa-solid fa-envelope'}
    ],
    'social': [
        {'id': 'wa-friend', 'title': 'The New-Number Friend', 'desc': 'Verify contact identities during money crises.', 'icon': 'fa-solid fa-comments'},
        {'id': 'dm-copyright', 'title': 'The Account Warning', 'desc': 'Ignore fake policy direct messages.', 'icon': 'fa-solid fa-user-shield'}
    ],
    'hacking': [
        {'id': 'scareware', 'title': 'The Virus Warning', 'desc': 'Identify deceptive browser system pop-ups.', 'icon': 'fa-solid fa-circle-exclamation'},
        {'id': 'wifi-snare', 'title': 'The Free Wi-Fi Snare', 'desc': 'Learn the risk of open public connections.', 'icon': 'fa-solid fa-wifi'}
    ],
    'misc': [
        {'id': 'job-scam', 'title': 'The Too-Easy Job', 'desc': 'Detect task-based career scams on messaging services.', 'icon': 'fa-solid fa-briefcase'},
        {'id': 'grandparent-call', 'title': 'The Urgent Phone Call', 'desc': 'Block family voice clone emergency hoaxes.', 'icon': 'fa-solid fa-phone-volume'}
    ]
}

# Detailed data for the five financial fraud types
FINANCIAL_FRAUDS = {
    'card-fraud': {
        'title': 'Credit/Debit Card Frauds',
        'desc': 'Protect card credentials and online transactions from theft.',
        'icon': 'fa-solid fa-credit-card',
        'class': 'color-fin',
        'how_it_works': [
            'Scammers use phishing emails, fake websites, or phone calls pretending to be bank staff to steal your 16-digit card number, CVV, and expiry date.',
            'They may use physical devices called skimmers placed over ATM card slots or store payment terminals to read your card chip or magnetic strip.',
            'With your card info and cloned data, they run unauthorized online transactions or duplicate cards to drain your account.'
        ],
        'warning_signs': [
            'Messages demanding your PIN, CVV, or card password "to prevent account suspension" (banks never ask for passwords/CVVs).',
            'Unfamiliar transactions—even tiny amounts—on your bank statement.',
            'ATM card slots that feel loose, bulky, or look altered.'
        ],
        'safety_tips': [
            'Never share your card PIN, CVV, or OTP with anyone, including bank representatives.',
            'Enable transaction limits and instant SMS/email alerts for all card transactions.',
            'Inspect ATM card slots before inserting your card, and cover the keypad when typing your PIN.',
            'Use virtual or one-time use cards for online purchases on new or unfamiliar websites.'
        ],
        'scenario_id': 'email-bank'
    },
    'upi-fraud': {
        'title': 'UPI Fraud',
        'desc': 'Avoid fake QR codes, UPI PIN traps, and collect requests.',
        'icon': 'fa-solid fa-mobile-screen-button',
        'class': 'color-fin',
        'phone_number': '+91 90876 12345',
        'phone_caller': 'UPI Assistance Bureau',
        'alert_tag': 'Collect Request Warning',
        'decline_warning': 'Declining this call is safe, but answer this simulated call to practice identifying UPI traps!',
        'dialogue': [
            "Hello! I am calling from the national UPI payments support helpdesk.",
            "We have flagged a pending 'debit authorization request' of ₹25,000 on your UPI profile.",
            "To decline and block this request, please scan the QR code I shared on your WhatsApp and input your UPI PIN now."
        ],
        'options': [
            { 'text': "✅ Okay, I will scan the QR and enter PIN to cancel.", 'action': 'share' },
            { 'text': "🤔 Why is a UPI PIN required to receive a refund or cancel a request?", 'action': 'ask_why' },
            { 'text': "❌ I won't scan or enter my PIN. Receiving money never requires a PIN.", 'action': 'refuse' }
        ],
        'aggressive_dialogue': [
            "Sir, if you don't input your PIN immediately, the debit request will auto-clear and ₹25,000 will be withdrawn from your account!",
            "This is your final warning! Enter the PIN now or lose the funds permanently!"
        ],
        'share_action_msg': "Processing cancellation... PIN accepted. Connection terminated.",
        'refuse_action_msg': "Fine! If you don't authenticate now, your account will be locked. [Caller hangs up...]",
        'scammed_explanation': {
            'mistake': "Scanning a QR code and typing your UPI PIN. A UPI PIN is a payment authorization key; it is only entered when sending money, never when receiving or canceling a debit request.",
            'what_was_stolen': "The scammer obtained your authorization signature (UPI PIN) and routed the funds instantly from your linked bank account."
        },
        'safe_explanation': [
            "PIN Safeguard: You recognized that entering a UPI PIN always debits funds, never credits them.",
            "Refused Scanning: You avoided scanning unknown QR codes which carry masked debit instructions.",
            "Direct Channel: You chose to use official payment provider channels rather than third-party callers."
        ],
        'badge_title': "UPI Fraud Awareness Completed",
        'emergency_checklist': [
            "Open your payment app and disable/reset your UPI PIN immediately",
            "Freeze your linked bank accounts and disable UPI services through net banking",
            "Report the transaction on the payment app support section (GPay/PhonePe/Paytm)",
            "Report the fraud on the National Cyber Crime Portal (cybercrime.gov.in)",
            "Call the national cyber helpline 1930 immediately",
            "File a formal dispute with your bank for the unauthorized transfer"
        ],
        'how_it_works': [
            { 'title': "Scammer Contacts", 'icon': "fa-solid fa-phone", 'desc': "Attacker contacts you claiming to solve a pending transaction." },
            { 'title': "Sends QR/Request", 'icon': "fa-solid fa-qrcode", 'desc': "Sends a WhatsApp QR code or triggers a 'Collect' request." },
            { 'title': "Creates Urgency", 'icon': "fa-solid fa-gauge-high", 'desc': "Claims money will be deducted if you do not act instantly." },
            { 'title': "Demands PIN", 'icon': "fa-solid fa-key", 'desc': "Asks you to scan and enter your UPI PIN to 'cancel'." },
            { 'title': "Authorizes Debit", 'icon': "fa-solid fa-receipt", 'desc': "The entered PIN clears the bank payment gateway." },
            { 'title': "Withdraws Funds", 'icon': "fa-solid fa-building-columns", 'desc': "Cash is instantly routed to the scammer's bank card." }
        ],
        'warning_signs': [
            { 'title': "PIN for Payouts", 'icon': "fa-solid fa-key", 'desc': "Entering your PIN to receive, cancel, or refund money." },
            { 'title': "WhatsApp QR Codes", 'icon': "fa-solid fa-qrcode", 'desc': "Receiving QR codes via chat apps to collect prize money." },
            { 'title': "Olx/Marketplace Buyers", 'icon': "fa-solid fa-store", 'desc': "Buyers who send QR codes to advance-pay you." },
            { 'title': "Collect Requests", 'icon': "fa-solid fa-bell", 'desc': "Sudden notifications asking you to approve a payment request." },
            { 'title': "Unverified Numbers", 'icon': "fa-solid fa-circle-exclamation", 'desc': "Helpdesk contacts on web searches that don't match bank details." }
        ],
        'quiz': [
            { 'question': "You receive an SMS: 'Scan this QR code to collect a cashback bonus of ₹500.'", 'answer': "scam", 'genuine_exp': "", 'scam_exp': "Correct! Scanning a QR code always prompts a debit or opens a payment gateway. Cashbacks are credited automatically, never via scanning." },
            { 'question': "Your UPI payment app prompts: 'Enter UPI PIN to approve payment of ₹2,500' for a merchant you are currently transacting with.", 'answer': "genuine", 'genuine_exp': "Correct! You only enter a PIN when you explicitly want to pay a merchant or transfer funds.", 'scam_exp': "" },
            { 'question': "A buyer on a marketplace app sends a screenshot showing a successful transfer to you, then requests you to enter your PIN to complete the clearance.", 'answer': "scam", 'genuine_exp': "", 'scam_exp': "Correct! Fake screenshots are common. Receiving money never requires entering your PIN." },
            { 'question': "You notice a notification on your UPI app for a 'Collect Request' of ₹5,000 from an unknown merchant, asking you to approve it.", 'answer': "scam", 'genuine_exp': "", 'scam_exp': "Correct! Decline all collect requests from unknown merchants. Approving them debits your account." },
            { 'question': "You scan a QR code at a retail shop to pay, and double-check that the merchant name displayed in the app matches the shop signboard.", 'answer': "genuine", 'genuine_exp': "Correct! Always verify merchant details on the screen before entering your PIN.", 'scam_exp': "" }
        ],
        'laws': [
            { 'title': "Information Technology Act", 'sub': "Section 66D – Impersonation", 'desc': "Penalizes cheating by impersonation using computer resources. Punishable by up to 3 years imprisonment and a ₹1 Lakh fine." },
            { 'title': "Information Technology Act", 'sub': "Section 43 – Unauthorized Access", 'desc': "Imposes damages for unauthorized data extraction or system tampering, covering hackers sending malicious links." },
            { 'title': "Bharatiya Nyaya Sanhita", 'sub': "Section 318 – Cheating", 'desc': "Prohibits deceitful inducement to deliver property. UPI scam operators are prosecuted under cheating provisions." },
            { 'title': "RBI Customer Protection Rules", 'sub': "Limited Liability", 'desc': "Protects customers from unauthorized electronic transactions if reported to bank authorities within 3 days." }
        ],
        'safety_tips': [
            { 'title': "PIN is to Send Only", 'icon': "fa-solid fa-key", 'desc': "Remember: PIN is only for sending money, never for receiving." },
            { 'title': "Verify Names First", 'icon': "fa-solid fa-signature", 'desc': "Check display names on screen before hitting send." },
            { 'title': "No QR for Refunds", 'icon': "fa-solid fa-qrcode", 'desc': "Refuse to scan QR codes shared for refunds or rewards." },
            { 'title': "Ignore Collect Requests", 'icon': "fa-solid fa-bell-slash", 'desc': "Decline unsolicited collect requests instantly." },
            { 'title': "Set Daily Limits", 'icon': "fa-solid fa-sliders", 'desc': "Keep transaction limits low to minimize potential loss." },
            { 'title': "Use Secure Connections", 'icon': "fa-solid fa-wifi", 'desc': "Avoid making payments on public or open Wi-Fi networks." }
        ],
        'prev_id': 'card-fraud',
        'next_id': 'job-fraud',
        'scenario_id': None
    },
    'job-fraud': {
        'title': 'Job Fraud',
        'desc': 'Identify fake job offers, work-from-home traps, and registration fees.',
        'icon': 'fa-solid fa-briefcase',
        'class': 'color-fin',
        'phone_number': '+91 97765 43210',
        'phone_caller': 'Career Growth Solutions HR',
        'alert_tag': 'Part-time Job Recruitment',
        'decline_warning': 'Declining this call is safe, but answer this simulated call to practice identifying job deposit scams!',
        'dialogue': [
            "Hello! I am contacting you from the Career Growth Solutions HR recruitment agency.",
            "We have exciting part-time work-from-home vacancies. You only need to review movies/likes on YouTube for 1 hour a day.",
            "You can easily earn ₹5,000 daily! To activate your recruiter account and start, please deposit a refundable registration fee of ₹2,500."
        ],
        'options': [
            { 'text': "✅ Okay, I will transfer the registration fee to start.", 'action': 'share' },
            { 'text': "🤔 Why must candidates pay registration fees to get hired?", 'action': 'ask_why' },
            { 'text': "❌ I won't pay. Legitimate companies never charge candidates.", 'action': 'refuse' }
        ],
        'aggressive_dialogue': [
            "Sir, this is a premium corporate tie-up. We charge this deposit to verify candidate commitment and issue software logs.",
            "If you don't transfer within 10 minutes, we will pass this vacancy to the next candidate on our waiting list!"
        ],
        'share_action_msg': "Payment received. Standby for HR activation keys... HR desk disconnected.",
        'refuse_action_msg': "Fine! Good luck finding a job elsewhere. [Caller hangs up...]",
        'scammed_explanation': {
            'mistake': "Paying an upfront fee to secure a job. Genuine employers never charge candidates for recruitment, training, or equipment deposits.",
            'what_was_stolen': "The scammer stole your registration deposit of ₹2,500 and will block your contact details instantly."
        },
        'safe_explanation': [
            "No Job Fees: You recognized that legitimate employers pay employees, they never charge them.",
            "Pressure Defied: You ignored the urgency tactic of 'giving the vacancy to another candidate'.",
            "Employer Audit: You refused to send money to private accounts for corporate recruitments."
        ],
        'badge_title': "Job Fraud Awareness Completed",
        'emergency_checklist': [
            "Report the beneficiary UPI/bank account to your bank to freeze transactions",
            "Flag the recruitment number on WhatsApp/Telegram as a job scam",
            "Take screenshots of the job offer, chats, and payment transactions",
            "Report the incident on National Cyber Crime Portal (cybercrime.gov.in)",
            "Call the national cyber helpline 1930 immediately",
            "Never pay additional 'withdrawal fees' if the scammers demand it to release commissions"
        ],
        'how_it_works': [
            { 'title': "Unsolicited Offer", 'icon': "fa-solid fa-briefcase", 'desc': "Scammer messages you on WhatsApp/Telegram with a high-paying job." },
            { 'title': "Initial Pay", 'icon': "fa-solid fa-hand-holding-dollar", 'desc': "Pays you small sums (like ₹150) for simple review tasks to build trust." },
            { 'title': "VIP Upgrade Trap", 'icon': "fa-solid fa-circle-up", 'desc': "Asks you to pay deposit/fee to upgrade to higher salary tier." },
            { 'title': "Commission Lock", 'icon': "fa-solid fa-lock", 'desc': "Locks your virtual wallet; claims you must pay 'tax' to withdraw cash." },
            { 'title': "Urgent Coercion", 'icon': "fa-solid fa-bell", 'desc': "Demands further payment to unlock access before a timer expires." },
            { 'title': "Account Blocked", 'icon': "fa-solid fa-user-slash", 'desc': "Attacker blocks your number and vanishes with all deposited cash." }
        ],
        'warning_signs': [
            { 'title': "Upfront Payments", 'icon': "fa-solid fa-wallet", 'desc': "Demanding cash for security, background checks, or laptop setups." },
            { 'title': "Unrealistic Pay", 'icon': "fa-solid fa-money-bill-wave", 'desc': "Offering massive pay (₹5,000/day) for low-skill tasks." },
            { 'title': "Chat App Interviews", 'icon': "fa-solid fa-comments", 'desc': "Hiring processes handled entirely via Telegram/WhatsApp text." },
            { 'title': "Commission Deposits", 'icon': "fa-solid fa-circle-down", 'desc': "Requiring you to invest money to withdraw commissions." },
            { 'title': "Generic Email Accounts", 'icon': "fa-solid fa-envelope", 'desc': "Recruiters using Gmail/Yahoo instead of corporate domains." }
        ],
        'quiz': [
            { 'question': "You get a Telegram message: 'Earn ₹300 per hour liking YouTube videos. Just deposit ₹1,000 to register.'", 'answer': "scam", 'genuine_exp': "", 'scam_exp': "Correct! Charging registration fees is a hallmark of task-based job scams." },
            { 'question': "A company invites you for an interview. The HR coordinator contacts you using an email domain like 'hr@tata.com' rather than a Gmail address.", 'answer': "genuine", 'genuine_exp': "Correct! Official recruiters write from official company domains.", 'scam_exp': "" },
            { 'question': "An online job portal asks you to pay a 'refundable check clearance fee' of ₹5,000 before they send you a company laptop.", 'answer': "scam", 'genuine_exp': "", 'scam_exp': "Correct! Real employers cover equipment costs and never charge candidates check fees." },
            { 'question': "A part-time job app shows you have earned ₹12,000 in task commission, but says you must pay ₹3,000 in 'customs clearance' to withdraw it.", 'answer': "scam", 'genuine_exp': "", 'scam_exp': "Correct! Demanding deposits to release earnings is a commission lock trap." },
            { 'question': "A local recruiter charges no fee, schedules a video interview, and requests your PAN/Aadhaar card details only after sending an official offer letter.", 'answer': "genuine", 'genuine_exp': "Correct! Official onboarding happens after interviews and requires no payment.", 'scam_exp': "" }
        ],
        'laws': [
            { 'title': "Information Technology Act", 'sub': "Section 66D – Personation", 'desc': "Covers fake profiles and impersonating HR representatives on messaging apps. Imposes up to 3 years jail." },
            { 'title': "Bharatiya Nyaya Sanhita", 'sub': "Section 319 – Impersonation", 'desc': "Penalizes cheating by pretending to be another person, such as a corporate officer. Carries up to 3 years imprisonment." },
            { 'title': "Bharatiya Nyaya Sanhita", 'sub': "Section 318 – Cheating", 'desc': "Punishes deceptive inducement to deliver funds under false pretense of job security." },
            { 'title': "Information Technology Act", 'sub': "Section 43(j) – Computer Contaminants", 'desc': "Applies if the fake recruiter sends spyware links disguised as job logging utilities." }
        ],
        'safety_tips': [
            { 'title': "Jobs Pay You", 'icon': "fa-solid fa-hand-holding-dollar", 'desc': "Never pay money to get a job. True employers pay employees." },
            { 'title': "Audit Recruiters", 'icon': "fa-solid fa-user-check", 'desc': "Look up recruiters on LinkedIn and verify their emails." },
            { 'title': "Avoid Task Groups", 'icon': "fa-solid fa-users-slash", 'desc': "Stay away from Telegram/WhatsApp groups offering 'likes' cash." },
            { 'title': "Never Fund Equipment", 'icon': "fa-solid fa-laptop", 'desc': "Companies provide laptops directly and never require deposits." },
            { 'title': "Report Fake Ads", 'icon': "fa-solid fa-bullhorn", 'desc': "Flag online listings promising fast earnings for review tasks." },
            { 'title': "Protect KYC Data", 'icon': "fa-solid fa-id-card", 'desc': "Only share PAN/Aadhaar details through verified portals." }
        ],
        'prev_id': 'upi-fraud',
        'next_id': 'lottery-fraud',
        'scenario_id': 'job-scam'
    },
    'lottery-fraud': {
        'title': 'Lottery Fraud',
        'desc': 'Recognize fake jackpot SMS, email notices, and processing fees.',
        'icon': 'fa-solid fa-gift',
        'class': 'color-fin',
        'phone_number': '+91 91122 33445',
        'phone_caller': 'KBC Prize Office',
        'alert_tag': 'Lucky Draw Notification',
        'decline_warning': 'Declining this call is safe, but answer this simulated call to practice identifying lottery scams!',
        'dialogue': [
            "Hello! I am calling from the KBC Lucky Draw Prize Distribution Office.",
            "Congratulations! Your phone number has won a mega lottery prize of ₹25 Lakhs!",
            "To release the prize money to your bank account, please pay a government processing tax of ₹15,000 immediately."
        ],
        'options': [
            { 'text': "✅ Okay, I will pay the processing tax to receive ₹25 Lakhs.", 'action': 'share' },
            { 'text': "🤔 Why should I pay taxes beforehand? Can't you deduct it from the prize?", 'action': 'ask_why' },
            { 'text': "❌ I won't pay. Real sweepstakes do not charge upfront fees.", 'action': 'refuse' }
        ],
        'aggressive_dialogue': [
            "Sir, under tax laws, lottery winnings cannot be cleared without prior state stamp duty verification.",
            "If you don't transfer the ₹15,000 within 15 minutes, we will cancel your draw and report your account to tax audits!"
        ],
        'share_action_msg': "Stamp duty received. Initiating transfer... Standby. KBC desk disconnected.",
        'refuse_action_msg': "Fine! You lose the ₹25 Lakhs. [Caller hangs up...]",
        'scammed_explanation': {
            'mistake': "Paying advance tax/processing fees to claim a prize. Real lotteries and luckydraws will never ask you to pay fees or taxes upfront to receive winnings.",
            'what_was_stolen': "The scammer stole your 'tax deposit' of ₹15,000 and will continue to ask for more fees under different names (conversion fee, clearance fee) until you stop paying."
        },
        'safe_explanation': [
            "No Advance Tax: You recognized that sweepstakes never charge upfront processing or stamp duty fees.",
            "Unentered Draws: You checked that you never bought any tickets or entered KBC draws.",
            "Tax Deduction Rules: You knew that legal taxes are deducted at source (TDS), not prepaid."
        ],
        'badge_title': "Lottery Fraud Awareness Completed",
        'emergency_checklist': [
            "Notify your bank to freeze the beneficiary account details immediately",
            "Block and report the sender number on WhatsApp/messaging apps",
            "Take screenshots of the prize letter, banner, and deposit transactions",
            "File an online complaint on the National Cyber Crime Portal (cybercrime.gov.in)",
            "Call the national cyber helpline 1930 immediately",
            "Never pay secondary clearance fees to recover initial losses"
        ],
        'how_it_works': [
            { 'title': "Jackpot Alert", 'icon': "fa-solid fa-gift", 'desc': "Scammer texts you claiming your number won a KBC or brand lucky draw." },
            { 'title': "Urgency Coercion", 'icon': "fa-solid fa-hourglass-half", 'desc': "Claims the draw expires in hours if you do not contact them." },
            { 'title': "Demands Tax", 'icon': "fa-solid fa-money-bill-wave", 'desc': "Asks you to deposit 'processing tax' or 'stamp duties' beforehand." },
            { 'title': "Manufactures Snags", 'icon': "fa-solid fa-triangle-exclamation", 'desc': "Claims customs or bank security stopped the transfer; asks for more cash." },
            { 'title': "Exhausts Funds", 'icon': "fa-solid fa-piggy-bank", 'desc': "Keeps demanding cash under different names until you run out." },
            { 'title': "Disappears", 'icon': "fa-solid fa-user-slash", 'desc': "Blocks your number and deletes all profiles once you realize the scam." }
        ],
        'warning_signs': [
            { 'title': "Unentered Draws", 'icon': "fa-solid fa-circle-question", 'desc': "Winning a lottery for a draw you never entered or bought tickets for." },
            { 'title': "Upfront Payments", 'icon': "fa-solid fa-file-invoice-dollar", 'desc': "Paying 'taxes', 'bank charges', or 'courier fees' to release winnings." },
            { 'title': "Chat App Banners", 'icon': "fa-solid fa-image", 'desc': "Receiving poorly designed prize posters with celebrity photos on WhatsApp." },
            { 'title': "Generic Email Senders", 'icon': "fa-solid fa-envelope", 'desc': "Lottery announcements from public addresses like Gmail or Yahoo." },
            { 'title': "Urgent Deadlines", 'icon': "fa-solid fa-clock", 'desc': "Threatening to cancel the prize unless fees are paid within hours." }
        ],
        'quiz': [
            { 'question': "You get a WhatsApp message: 'Congratulations! Your number won the KBC ₹25 Lakh lottery. Call this number to claim.'", 'answer': "scam", 'genuine_exp': "", 'scam_exp': "Correct! KBC does not hold lucky draws for random phone numbers over WhatsApp." },
            { 'question': "You buy a sweepstakes ticket at a retail store, write your name on the receipt stub, and deposit it in a physical drop-box.", 'answer': "genuine", 'genuine_exp': "Correct! This is a physical, verifiable sweepstakes entry.", 'scam_exp': "" },
            { 'question': "An email says you won ₹10 Crores from Coca-Cola and must transfer ₹20,000 for customs clearance before they ship the cheque.", 'answer': "scam", 'genuine_exp': "", 'scam_exp': "Correct! Real corporations do not charge winners customs fees or processing charges." },
            { 'question': "You receive an email from your state lottery board with a link to check winning numbers matching your physical ticket stub.", 'answer': "genuine", 'genuine_exp': "Correct! Checking winning tickets on official portal domains is safe.", 'scam_exp': "" },
            { 'question': "A caller tells you that you won a car in a brand lucky draw and asks you to pay ₹25,000 for 'registration and insurance' before delivery.", 'answer': "scam", 'genuine_exp': "", 'scam_exp': "Correct! Delivery or insurance charges are common tricks to extract advance money." }
        ],
        'laws': [
            { 'title': "Information Technology Act", 'sub': "Section 66D – Computer Cheating", 'desc': "Covers digital lottery fraud emails and messages. Imposes up to 3 years imprisonment and ₹1 Lakh fine." },
            { 'title': "Bharatiya Nyaya Sanhita", 'sub': "Section 318 – Cheating", 'desc': "Prosecutes scammers for creating fake lotteries to induce victims to transfer cash." },
            { 'title': "Indian Contract Act, 1872", 'sub': "Section 30 – Wagering", 'desc': "Governs lottery contracts. Declares wagering agreements void, making scam lotteries legally unenforceable." },
            { 'title': "Consumer Protection Act, 2019", 'sub': "Unfair Trade Practices", 'desc': "Outlaws deceptive contests and lucky draws that mislead consumers." }
        ],
        'safety_tips': [
            { 'title': "No Fees for Prizes", 'icon': "fa-solid fa-gift", 'desc': "Remember: Legal lotteries never charge upfront fees to winners." },
            { 'title': "Ignore Unentered Draws", 'icon': "fa-solid fa-circle-question", 'desc': "If you did not buy a ticket, you cannot win a prize." },
            { 'title': "Prepaid Taxes are Fake", 'icon': "fa-solid fa-file-invoice", 'desc': "Taxes are deducted from winnings, not pre-paid." },
            { 'title': "Check Official Portals", 'icon': "fa-solid fa-globe", 'desc': "Verify contests only on official company websites." },
            { 'title': "Delete WhatsApp Banners", 'icon': "fa-solid fa-trash-can", 'desc': "Discard all random lucky draw flyers instantly." },
            { 'title': "Secure Contact Portals", 'icon': "fa-solid fa-phone", 'desc': "Call official support numbers to verify brand contests." }
        ],
        'prev_id': 'job-fraud',
        'next_id': 'sim-swapping',
        'scenario_id': 'sms-lottery'
    },
    'sim-swapping': {
        'title': 'SIM Swapping',
        'desc': 'Prevent hackers from taking over your mobile phone number.',
        'icon': 'fa-solid fa-sim-card',
        'class': 'color-fin',
        'phone_number': '+91 90000 11223',
        'phone_caller': 'Telecom Service Bureau',
        'alert_tag': 'SIM Upgrade Notification',
        'decline_warning': 'Declining this call is safe, but answer this simulated call to practice identifying SIM upgrade scams!',
        'dialogue': [
            "Hello! I am calling from your mobile service provider's network team.",
            "We are upgrading all regional SIM cards to 5G to prevent network termination.",
            "To upgrade your connection immediately, please reply '1' to the SMS I just sent and verify your eSIM code."
        ],
        'options': [
            { 'text': "✅ Okay, I will reply '1' and share the code.", 'action': 'share' },
            { 'text': "🤔 Why does an eSIM upgrade require replying to an SMS verification?", 'action': 'ask_why' },
            { 'text': "❌ I won't reply or share any codes. I will visit the store directly.", 'action': 'refuse' }
        ],
        'aggressive_dialogue': [
            "Sir, if you don't verify now, your mobile connection will be blocked within 30 minutes, and restoring service will take 48 hours!",
            "This is an urgent security upgrade. Please verify the code immediately!"
        ],
        'share_action_msg': "SIM upgrade code accepted. Activating new card logs... Connection terminated.",
        'refuse_action_msg': "Fine! Your network will be cut. [Caller hangs up...]",
        'scammed_explanation': {
            'mistake': "Replying '1' to carrier switch messages or sharing eSIM activation codes. This authorizes your carrier to disable your physical SIM and transfer your number to the scammer's eSIM.",
            'what_was_stolen': "The scammer hijacked your phone number. Your phone will lose signal, and the attacker will receive all your OTPs to reset banking accounts."
        },
        'safe_explanation': [
            "No eSIM Codes: You refused to share eSIM barcodes or carrier transfer approval SMS codes.",
            "Signal Loss Vigilance: You chose to contact the carrier directly through official customer service channels.",
            "Strict Verification: You recognized that telecoms do not swap SIM cards over phone calls."
        ],
        'badge_title': "SIM Swap Awareness Completed",
        'emergency_checklist': [
            "Contact your mobile carrier customer service immediately to block the SIM swap",
            "Call your bank customer support to block netbanking and card authorizations",
            "Notify your family that your phone number has been hijacked",
            "Check your bank accounts for unauthorized transfers once service is restored",
            "Report the SIM swap fraud on National Cyber Crime Portal (cybercrime.gov.in)",
            "Call the national cyber helpline 1930 immediately"
        ],
        'how_it_works': [
            { 'title': "Data Gathering", 'icon': "fa-solid fa-user-shield", 'desc': "Scammer harvests your name and bank profile through phishing or public data." },
            { 'title': "Carrier Trap Call", 'icon': "fa-solid fa-phone", 'desc': "Calls claiming to upgrade your SIM to 5G or prevent suspension." },
            { 'title': "Transfer SMS", 'icon': "fa-solid fa-message", 'desc': "Asks you to reply '1' or read eSIM codes to approve carrier transfer." },
            { 'title': "Signal Cut", 'icon': "fa-solid fa-signal", 'desc': "Your physical SIM is deactivated; your phone goes into 'No Service'." },
            { 'title': "OTP Theft", 'icon': "fa-solid fa-key", 'desc': "Attacker activates your number on their device and receives all bank OTPs." },
            { 'title': "Account Drained", 'icon': "fa-solid fa-building-columns", 'desc': "Scammer resets bank passwords and empties accounts using hijacked OTPs." }
        ],
        'warning_signs': [
            { 'title': "Sudden 'No Service'", 'icon': "fa-solid fa-signal-harm", 'desc': "Mobile connection suddenly cutting out in good signal areas." },
            { 'title': "Carrier Swapping SMS", 'icon': "fa-solid fa-message", 'desc': "Alerts confirming a SIM swap or eSIM request you didn't initiate." },
            { 'title': "OTP Validation", 'icon': "fa-solid fa-key", 'desc': "Callers asking you to approve a carrier transfer via text replies." },
            { 'title': "eSIM QR Requests", 'icon': "fa-solid fa-qrcode", 'desc': "Requests to share QR barcodes sent by your service provider." },
            { 'title': "Unsolicited Calls", 'icon': "fa-solid fa-circle-phone", 'desc': "Helpdesk callers demanding details to 'upgrade' your network tier." }
        ],
        'quiz': [
            { 'question': "Your mobile phone suddenly displays 'No Service' and won't connect even after restarting. You contact your carrier support instantly.", 'answer': "genuine", 'genuine_exp': "Correct! Sudden service loss is a key warning sign of ongoing SIM swaps; immediate response blocks bank hijack attempts.", 'scam_exp': "" },
            { 'question': "A caller from 'Telecom Support' asks you to read out a 32-character eSIM activation string sent to your email to verify your connection.", 'answer': "scam", 'genuine_exp': "", 'scam_exp': "Correct! Legitimate service providers never ask you to read out eSIM activation codes." },
            { 'question': "You receive an SMS: 'A SIM replacement request has been initiated. Reply 1 within 10 minutes to approve, or 2 to decline.'", 'answer': "scam", 'genuine_exp': "", 'scam_exp': "Correct! Scammers trigger SIM replacements and try to trick you into approving them via SMS replies." },
            { 'question': "You visit your mobile carrier's official branch in person, present your ID proof, and collect a physical replacement SIM card.", 'answer': "genuine", 'genuine_exp': "Correct! Physical SIM replacement at official stores is the safest practice.", 'scam_exp': "" },
            { 'question': "A caller tells you that they can upgrade your 4G SIM to 5G remotely if you forward a specific carrier configuration SMS to their number.", 'answer': "scam", 'genuine_exp': "", 'scam_exp': "Correct! Remote 5G upgrade requests are common tricks to hijack SMS forwarding configurations." }
        ],
        'laws': [
            { 'title': "Information Technology Act", 'sub': "Section 66C – Identity Theft", 'desc': "Swapping a SIM to hijack numbers constitutes identity theft. Imposes up to 3 years imprisonment and a ₹1 Lakh fine." },
            { 'title': "Information Technology Act", 'sub': "Section 66D – Impersonation", 'desc': "Covers fake telecom caller identification used to extract eSIM details. Punishable with up to 3 years jail." },
            { 'title': "Bharatiya Nyaya Sanhita", 'sub': "Identity Fraud", 'desc': "BNS section penalizing the fraudulent use of identity details to obtain cellular profile swaps." },
            { 'title': "TRAI Subscriber Regulations", 'sub': "SIM Swapping Limits", 'desc': "Telecom regulations requiring physical verification and imposing limits on eSIM activation timing." }
        ],
        'safety_tips': [
            { 'title': "SIM swaps are in-store", 'icon': "fa-solid fa-store", 'desc': "Only request SIM swaps or eSIM activation inside official carrier branches." },
            { 'title': "Never Read eSIM codes", 'icon': "fa-solid fa-qrcode", 'desc': "eSIM codes are network profiles. Never share them with anyone." },
            { 'title': "Report Sudden Service Cuts", 'icon': "fa-solid fa-signal", 'desc': "Contact your carrier instantly if you experience sudden 'No Service'." },
            { 'title': "Lock SIM PIN", 'icon': "fa-solid fa-key", 'desc': "Set a custom carrier PIN/passcode to block SIM swap authorizations." },
            { 'title': "Protect personal info", 'icon': "fa-solid fa-user-shield", 'desc': "Don't share names, birthdays, and emails on public social media." },
            { 'title': "Add Bank Alerts", 'icon': "fa-solid fa-bell", 'desc': "Register email alerts for bank transactions in case SMS is hijacked." }
        ],
        'prev_id': 'lottery-fraud',
        'next_id': None,
        'scenario_id': None
    }
}

# ──────────────────────────────────────────────
# Social Media Crimes detailed data
# ──────────────────────────────────────────────
SOCIAL_MEDIA_CRIMES = {
    'csam': {
        'title': 'Child Sexual Abuse Material (CSAM)',
        'desc': 'Recognise, refuse, and report illegal content involving children circulated through messaging apps and social platforms.',
        'icon': 'fa-solid fa-child-reaching',
        'class': 'color-soc',
        'real_situation': {
            'platform': 'WhatsApp Group',
            'platform_icon': 'fa-brands fa-whatsapp',
            'platform_color': '#25D366',
            'group_name': 'Old School Batch',
            'time': '11:48 PM',
            'chat': [
                {'sender': 'Rajan Mehta', 'avatar': 'R', 'side': 'received',
                 'text': 'Hey guys, check this clip someone shared in the locality group', 'time': '11:45 PM'},
                {'sender': 'Rajan Mehta', 'avatar': 'R', 'side': 'received',
                 'text': '[Video Attachment - 3.2 MB]', 'time': '11:46 PM', 'media': 'video'},
                {'sender': 'Priya K', 'avatar': 'P', 'side': 'received',
                 'text': 'This looks like it involves a minor. This is illegal content.', 'time': '11:47 PM'},
                {'sender': 'Rajan Mehta', 'avatar': 'R', 'side': 'received',
                 'text': "Relax, just forward it. Everyone is sharing it anyway. Don't be boring.", 'time': '11:48 PM'},
            ],
            'decision_prompt': 'You received an attachment in a group chat that appears to contain illegal content involving a child. A contact is pressuring you to forward it. What do you do?',
            'decision_options': [
                {'label': 'Forward the video to other contacts as asked', 'correct': False,
                 'feedback': 'Forwarding, downloading, or saving CSAM is a criminal offence under POCSO and IT Act, even if you received it accidentally.'},
                {'label': 'Ignore the message and stay silent', 'correct': False,
                 'feedback': 'Staying silent allows the abuse to continue. You must report the content and exit the group.'},
                {'label': 'Report the content to the platform and cybercrime.gov.in immediately', 'correct': True,
                 'feedback': 'Correct! Do NOT open, save, or forward the content. Use the report feature on WhatsApp, then file a report at cybercrime.gov.in or call 1930.'},
            ]
        },
        'alert_tag': 'Illegal Content Group Alert',
        'phone_number': 'WhatsApp Group Chat',
        'phone_caller': 'Old School Batch Group',
        'decline_warning': 'Leaving this group is safe, but engage with this simulation to learn how to respond to CSAM in group chats.',
        'dialogue': [
            'Hey! Someone just dropped a video in our locality group. Looks really bad involving a child.',
            'I forwarded it here by mistake. Can you help me figure out what to do with it?',
            "My friend says just delete it and move on. But another person says we should share it to raise awareness. What do you think?"
        ],
        'options': [
            {'text': 'Share it to raise awareness as suggested.', 'action': 'share'},
            {'text': 'Why would sharing this content be a problem even with good intent?', 'action': 'ask_why'},
            {'text': 'Do NOT share it. Report it to the platform and cybercrime.gov.in immediately.', 'action': 'refuse'}
        ],
        'aggressive_dialogue': [
            "But people need to know this is happening! Isn't raising awareness important?",
            "Fine, but at least save it as evidence before reporting, right?"
        ],
        'share_action_msg': "Content forwarded. Sharing CSAM even with good intent is a criminal act under Indian law.",
        'refuse_action_msg': "Okay. I'll just delete it then and pretend it never happened.",
        'scammed_explanation': {
            'mistake': 'Forwarding, saving, or sharing child sexual abuse material — even with the intent to raise awareness — is a cognizable, non-bailable criminal offence under POCSO Act and IT Act.',
            'what_was_stolen': 'You exposed yourself to serious criminal prosecution. Your device IP, phone number, and forward chain are traceable by cybercrime units.'
        },
        'safe_explanation': [
            'Report First: You used the in-app report feature to flag the content to the platform for immediate removal.',
            'No Forwarding: You did not forward, save, or screenshot the illegal material, keeping yourself legally protected.',
            'Cyber Helpline: You filed a report at cybercrime.gov.in and/or called 1930 so law enforcement can act.'
        ],
        'badge_title': 'CSAM Awareness Completed',
        'emergency_checklist': [
            'Do NOT open, download, save, or forward the content',
            'Use the report/flag feature on the platform (WhatsApp > Report > Child Safety)',
            'Exit or mute the group immediately to avoid further exposure',
            'File a report on cybercrime.gov.in under the child safety category',
            'Call the national cyber helpline 1930 immediately',
            'Clear your device cache so you do not inadvertently store the file'
        ],
        'how_it_works': [
            {'title': 'Content Created', 'icon': 'fa-solid fa-camera', 'desc': 'Abusers record illegal material involving minors and upload it to private groups or encrypted chats.'},
            {'title': 'Shared in Groups', 'icon': 'fa-solid fa-share-nodes', 'desc': 'Material is spread through messaging groups using peer pressure to normalize forwarding.'},
            {'title': 'Social Pressure', 'icon': 'fa-solid fa-people-arrows', 'desc': 'Contacts urge others to forward it under the guise of awareness, curiosity, or humor.'},
            {'title': 'Legal Trap', 'icon': 'fa-solid fa-gavel', 'desc': 'Every person who forwards or stores the content becomes liable under POCSO and IT Act.'},
            {'title': 'Device Evidence', 'icon': 'fa-solid fa-mobile-screen', 'desc': 'Cybercrime units trace the forward chain through device IPs and phone numbers.'},
            {'title': 'Criminal Charges', 'icon': 'fa-solid fa-handcuffs', 'desc': 'Recipients who shared the material face arrest, imprisonment, and lifelong stigma.'}
        ],
        'warning_signs': [
            {'title': 'Unknown Group Additions', 'icon': 'fa-solid fa-user-plus', 'desc': 'Being added to unknown groups sharing explicit or disturbing content.'},
            {'title': 'Peer Pressure to Forward', 'icon': 'fa-solid fa-share', 'desc': 'Contacts pushing you to forward content as a joke or for awareness.'},
            {'title': 'Encrypted-Only Groups', 'icon': 'fa-solid fa-lock', 'desc': 'Groups that advertise private or secret content sharing spaces online.'},
            {'title': 'Anonymous Senders', 'icon': 'fa-solid fa-user-secret', 'desc': 'Content originating from unknown, recently-created, or unverified accounts.'},
            {'title': 'Awareness Justification', 'icon': 'fa-solid fa-bullhorn', 'desc': 'Using social awareness or curiosity as an excuse to share illegal material.'}
        ],
        'quiz': [
            {'question': 'You receive a video in a WhatsApp group that appears to involve a minor in a sexual context. Your friend says to just delete it and move on. What should you do?', 'answer': 'scam', 'genuine_exp': '', 'scam_exp': 'Correct! Simply deleting is insufficient. You must report it on the platform and to cybercrime.gov.in so authorities can act.'},
            {'question': 'Someone in your group asks you to forward an explicit video to raise awareness about child abuse. You should forward it as requested.', 'answer': 'scam', 'genuine_exp': '', 'scam_exp': 'Correct! Forwarding CSAM under any pretext is a criminal act. Report the person who shared it instead.'},
            {'question': 'You accidentally receive a file that looks like CSAM. You immediately report it using the platform abuse report feature without opening or saving it.', 'answer': 'genuine', 'genuine_exp': 'Correct! Reporting without viewing or forwarding is exactly the right action to take.', 'scam_exp': ''},
            {'question': 'A contact says they found this content online and saved it as evidence to show police. They ask you to also save it first before reporting.', 'answer': 'scam', 'genuine_exp': '', 'scam_exp': 'Correct! Do not save the content. Report via cybercrime.gov.in — the platform servers retain records that law enforcement can access.'},
            {'question': "Your school's official child safety officer contacts you via school email and asks you to report suspicious online content to a verified government portal.", 'answer': 'genuine', 'genuine_exp': 'Correct! Verified authority contacts from official channels directing you to official portals are legitimate.', 'scam_exp': ''}
        ],
        'laws': [
            {'title': 'POCSO Act, 2012', 'sub': 'Section 13 and 15 - Child Pornography', 'desc': 'Prohibits using children in sexual content. Storing, viewing, or distributing CSAM carries up to 7 years imprisonment and heavy fines.'},
            {'title': 'Information Technology Act', 'sub': 'Section 67B - Child Explicit Material', 'desc': 'Publishing or transmitting sexually explicit material involving children online is punishable by up to 7 years jail on first conviction.'},
            {'title': 'Bharatiya Nyaya Sanhita', 'sub': 'Section 294 - Obscene Acts', 'desc': 'Penalizes the distribution or exhibition of obscene material, including through digital means, with imprisonment.'},
            {'title': 'IT Intermediary Guidelines', 'sub': 'Rule 3(1)(b)(iv)', 'desc': 'Platforms must disable and remove CSAM within 24 hours of detection. Users can trigger this by using the in-app report feature.'}
        ],
        'safety_tips': [
            {'title': 'Report, Do Not Forward', 'icon': 'fa-solid fa-flag', 'desc': 'Always report illegal content using the platform built-in report feature before doing anything else.'},
            {'title': 'Exit Unknown Groups', 'icon': 'fa-solid fa-right-from-bracket', 'desc': 'Leave and report groups that share disturbing or suspicious content immediately.'},
            {'title': 'Use cybercrime.gov.in', 'icon': 'fa-solid fa-globe', 'desc': 'File a formal report on the National Cyber Crime Reporting Portal for child safety violations.'},
            {'title': 'Never Store the Content', 'icon': 'fa-solid fa-ban', 'desc': 'Do not screenshot, download, or save the material — it makes you legally liable.'},
            {'title': 'Parental Controls', 'icon': 'fa-solid fa-shield-child', 'desc': 'Enable parental controls and digital literacy discussions to protect children in your family.'},
            {'title': 'Call 1930', 'icon': 'fa-solid fa-phone', 'desc': 'Contact the national cyber helpline immediately for any online content involving children.'}
        ],
        'prev_id': None,
        'next_id': 'sexually-explicit'
    },
    'sexually-explicit': {
        'title': 'Sexually Explicit Content and Sextortion',
        'desc': 'Understand how intimate image threats and AI-generated deepfakes are used to blackmail victims online.',
        'icon': 'fa-solid fa-eye-slash',
        'class': 'color-soc',
        'real_situation': {
            'platform': 'Instagram DM',
            'platform_icon': 'fa-brands fa-instagram',
            'platform_color': '#E1306C',
            'group_name': 'alex_photo_studio',
            'time': '9:15 PM',
            'chat': [
                {'sender': 'alex_photo_studio', 'avatar': 'A', 'side': 'received',
                 'text': "Hi! I'm a photographer at a local media agency. Your profile looks great!", 'time': '8:55 PM'},
                {'sender': 'alex_photo_studio', 'avatar': 'A', 'side': 'received',
                 'text': "We're looking for models for a private shoot campaign. Paid Rs.8,000 per day. Interested?", 'time': '8:57 PM'},
                {'sender': 'You', 'avatar': 'Y', 'side': 'sent',
                 'text': 'That sounds interesting! What does the campaign involve?', 'time': '9:00 PM'},
                {'sender': 'alex_photo_studio', 'avatar': 'A', 'side': 'received',
                 'text': "It's for an adult fashion brand. To confirm your spot, we need a few reference photos first — just casual ones for portfolio selection.", 'time': '9:10 PM'},
                {'sender': 'alex_photo_studio', 'avatar': 'A', 'side': 'received',
                 'text': "Don't worry — these are strictly confidential and only seen by the selection panel.", 'time': '9:15 PM'},
            ],
            'decision_prompt': 'A stranger on Instagram is offering paid modelling work and asking you to send private photos as a portfolio requirement. What do you do?',
            'decision_options': [
                {'label': 'Send the private photos as requested for the modelling selection', 'correct': False,
                 'feedback': 'This is a sextortion trap. Once you send intimate images, the scammer will use them to blackmail you for money or more explicit content.'},
                {'label': 'Continue chatting and ask for the agency website first', 'correct': False,
                 'feedback': "Continuing to engage keeps you in the scammer's trap. A fake website can easily be fabricated. Stop contact and report the account instead."},
                {'label': 'Refuse, block the account, and report it for sextortion', 'correct': True,
                 'feedback': 'Correct! Legitimate agencies never ask for private photos over DMs. Block and report the account. If threatened, report to cybercrime.gov.in and call 1930.'},
            ]
        },
        'alert_tag': 'Instagram DM - Modelling Offer',
        'phone_number': '@alex_photo_studio',
        'phone_caller': 'Fake Talent Scout',
        'decline_warning': 'Ignoring this DM is safe, but engage with this simulation to learn how sextortion traps are set.',
        'dialogue': [
            "Hi! I found your Instagram profile and I think you have amazing potential for our brand campaign.",
            "We are casting for a premium adult fashion line. The pay is Rs.8,000 per day and the shoot is fully confidential.",
            "To confirm your selection, we just need a few private reference photos first. This is standard procedure — we keep everything strictly private."
        ],
        'options': [
            {'text': 'Okay, I will send private photos as requested.', 'action': 'share'},
            {'text': 'Why do you need private photos over Instagram DM for selection?', 'action': 'ask_why'},
            {'text': 'I refuse. This is a sextortion trap. I will block and report this account.', 'action': 'refuse'}
        ],
        'aggressive_dialogue': [
            "This is perfectly legal — it's just a standard portfolio procedure. Other models have already sent theirs!",
            "Fine, but let me remind you — I already have your profile picture and can create content from it using AI tools."
        ],
        'share_action_msg': "Photos received. Your images are now in our system... [Account goes silent — contact is now blocked]",
        'refuse_action_msg': "You'll regret not taking this opportunity. [Scammer disconnects]",
        'scammed_explanation': {
            'mistake': 'Sending intimate or private images to an unverified stranger on social media. Legitimate agencies never request private photos over DMs.',
            'what_was_stolen': 'The scammer now possesses your private images and will use them to demand money, more explicit content, or public humiliation as leverage.'
        },
        'safe_explanation': [
            'Refused Image Sharing: You did not send any private content to an unverified stranger on social media.',
            'Identity Check: You recognized that real agencies use official emails, websites, and in-person casting calls — not Instagram DMs.',
            'Reported and Blocked: You removed the threat by reporting the account and preventing further contact.'
        ],
        'badge_title': 'Sextortion Awareness Completed',
        'emergency_checklist': [
            'Do not pay any money — paying only invites more demands',
            'Block the scammer on all platforms immediately',
            'Preserve screenshots of all conversations as evidence',
            "Report the account using the platform's in-app abuse reporting tool",
            'File a report on cybercrime.gov.in under the Women/Child Safety category',
            'Call the national cyber helpline 1930 for immediate assistance'
        ],
        'how_it_works': [
            {'title': 'Luring Contact', 'icon': 'fa-solid fa-fish-fins', 'desc': 'Scammer creates a fake profile pretending to be a talent scout, photographer, or admirer.'},
            {'title': 'Trust Building', 'icon': 'fa-solid fa-handshake', 'desc': 'Engages the victim in flattering conversation to build fake credibility and rapport.'},
            {'title': 'Image Request', 'icon': 'fa-solid fa-camera', 'desc': 'Requests private or intimate photos under the guise of a job, campaign, or relationship.'},
            {'title': 'Threat Issued', 'icon': 'fa-solid fa-triangle-exclamation', 'desc': 'Once images are received, the scammer threatens to leak them to family, friends, or online.'},
            {'title': 'Ransom Demand', 'icon': 'fa-solid fa-money-bill-wave', 'desc': 'Victim is forced to pay money or send more explicit content to prevent the release.'},
            {'title': 'Cycle Repeats', 'icon': 'fa-solid fa-rotate', 'desc': 'Payments are never enough — demands escalate until the victim cuts contact or reports.'}
        ],
        'warning_signs': [
            {'title': 'DM Job Offers', 'icon': 'fa-solid fa-briefcase', 'desc': 'Unsolicited modelling or acting offers arriving via social media direct messages.'},
            {'title': 'Private Photo Requests', 'icon': 'fa-solid fa-image', 'desc': 'Requests for intimate or private images as part of a selection or verification process.'},
            {'title': 'No Official Channel', 'icon': 'fa-solid fa-building', 'desc': 'Legitimate agencies never recruit or request content exclusively over DMs.'},
            {'title': 'AI Deepfake Threats', 'icon': 'fa-solid fa-robot', 'desc': 'Threats to create fake explicit images using your public profile pictures with AI tools.'},
            {'title': 'Urgency and Secrecy', 'icon': 'fa-solid fa-user-secret', 'desc': 'Being asked to keep the interaction secret and respond quickly before the offer expires.'}
        ],
        'quiz': [
            {'question': 'An Instagram DM from an unknown account offers you Rs.10,000 per day for a modelling campaign and asks for private photos to confirm your spot.', 'answer': 'scam', 'genuine_exp': '', 'scam_exp': 'Correct! Real modelling agencies use official emails and in-person auditions, never DM requests for private photos.'},
            {'question': 'A verified brand page on Instagram sends you a DM with their official website, agency email, and physical address for an audition walkthrough.', 'answer': 'genuine', 'genuine_exp': 'Correct! Verifiable contact details and official channels are signs of a legitimate opportunity.', 'scam_exp': ''},
            {'question': 'Someone online threatens to leak edited or AI-generated explicit images of you unless you pay Rs.5,000 within 2 hours.', 'answer': 'scam', 'genuine_exp': '', 'scam_exp': 'Correct! This is sextortion. Do not pay. Report to cybercrime.gov.in and call 1930 immediately.'},
            {'question': 'You receive intimate images of yourself that you never sent to anyone, edited using AI. The sender demands payment or they will share these images widely.', 'answer': 'scam', 'genuine_exp': '', 'scam_exp': 'Correct! AI-generated deepfake blackmail is a crime. Preserve evidence and file a complaint at cybercrime.gov.in.'},
            {'question': "A known friend from your college shares a verified brand's open casting call post on Instagram Stories with the brand's official website link.", 'answer': 'genuine', 'genuine_exp': 'Correct! Shared by a known contact with verified source links — this is a legitimate referral.', 'scam_exp': ''}
        ],
        'laws': [
            {'title': 'Information Technology Act', 'sub': 'Section 66E - Privacy Violation', 'desc': 'Capturing or transmitting intimate images without consent is punishable by up to 3 years imprisonment and Rs.2 Lakh fine.'},
            {'title': 'Information Technology Act', 'sub': 'Section 67A - Explicit Material', 'desc': 'Publishing sexually explicit material electronically carries imprisonment up to 5 years and fine on first offence.'},
            {'title': 'Bharatiya Nyaya Sanhita', 'sub': 'Section 77 - Voyeurism', 'desc': "Penalizes capturing or distributing intimate images without the subject's consent, carrying 3 to 7 years imprisonment."},
            {'title': 'Bharatiya Nyaya Sanhita', 'sub': 'Section 351 - Criminal Intimidation', 'desc': 'Threatening to circulate intimate images to extract money or compliance constitutes criminal intimidation.'}
        ],
        'safety_tips': [
            {'title': 'Never Share Privately', 'icon': 'fa-solid fa-eye-slash', 'desc': 'Never send intimate images to anyone online, regardless of the platform or relationship.'},
            {'title': 'Verify Before Engaging', 'icon': 'fa-solid fa-magnifying-glass', 'desc': "Always verify an agency's official website, address, and contact before responding to job offers."},
            {'title': 'Do Not Pay Ransom', 'icon': 'fa-solid fa-ban', 'desc': 'If threatened, do not pay — payments escalate demands. Report and block instead.'},
            {'title': 'Tighten Privacy Settings', 'icon': 'fa-solid fa-lock', 'desc': 'Keep social media accounts private to reduce exposure to unknown contacts.'},
            {'title': 'Screenshot Evidence', 'icon': 'fa-solid fa-camera', 'desc': 'Preserve all conversation screenshots before reporting or blocking the attacker.'},
            {'title': 'Helpline 1930', 'icon': 'fa-solid fa-phone', 'desc': 'Call the cyber helpline immediately. Sextortion is a crime — you are a victim, not at fault.'}
        ],
        'prev_id': 'csam',
        'next_id': 'obscene-content'
    },
    'obscene-content': {
        'title': 'Obscene Content and Peer Pressure Sharing',
        'desc': 'Learn how to handle online peer pressure to view, share, or forward obscene memes, videos, or images.',
        'icon': 'fa-solid fa-photo-film',
        'class': 'color-soc',
        'real_situation': {
            'platform': 'WhatsApp Group',
            'platform_icon': 'fa-brands fa-whatsapp',
            'platform_color': '#25D366',
            'group_name': 'College Gang',
            'time': '3:22 PM',
            'chat': [
                {'sender': 'Arjun S', 'avatar': 'A', 'side': 'received',
                 'text': 'Guys check this out, got it from Telegram', 'time': '3:15 PM', 'media': 'video'},
                {'sender': 'Neha T', 'avatar': 'N', 'side': 'received',
                 'text': 'OMG forward this to the hostel group too!', 'time': '3:17 PM'},
                {'sender': 'Arjun S', 'avatar': 'A', 'side': 'received',
                 'text': "Forward kar do — everyone's sharing it in all the college groups.", 'time': '3:20 PM'},
                {'sender': 'Arjun S', 'avatar': 'A', 'side': 'received',
                 'text': "Don't be a killjoy. It's just harmless fun. If you don't forward it, you're boring.", 'time': '3:22 PM'},
            ],
            'decision_prompt': 'Your friends are pressuring you to forward obscene content in your college group chat, calling it harmless fun. What do you do?',
            'decision_options': [
                {'label': 'Forward it to other groups — everyone is doing it anyway', 'correct': False,
                 'feedback': 'Forwarding obscene content — even when everyone is doing it — exposes you to legal liability under the IT Act and can harm real people in the content.'},
                {'label': "Watch it but don't forward — just stay quiet", 'correct': False,
                 'feedback': 'Staying silent normalizes the behavior. Muting and exiting the conversation is better, and reporting protects others.'},
                {'label': 'Refuse to forward, exit the conversation, and report if it involves real people', 'correct': True,
                 'feedback': 'Correct! Refusing peer pressure and reporting obscene content is the responsible action. Report to cybercrime.gov.in if it involves real people.'},
            ]
        },
        'alert_tag': 'WhatsApp Group - Content Forwarding',
        'phone_number': 'College Gang Group Chat',
        'phone_caller': 'Peer Pressure Scenario',
        'decline_warning': 'Exiting this simulation is safe, but engage with it to practice resisting peer pressure to share obscene content.',
        'dialogue': [
            "Hey! Check out this reel from Telegram — everyone in all the hostel groups is forwarding it.",
            "Come on, just forward it to the main batch group. It's just a funny meme — no big deal!",
            "Why are you being so uptight? It's just harmless fun. If you don't send it, we'll think you're scared of a joke."
        ],
        'options': [
            {"text": "Sure, I'll forward it to the main group.", 'action': 'share'},
            {'text': 'What kind of content is it exactly? Why is it only on Telegram?', 'action': 'ask_why'},
            {"text": "I won't forward it. Peer pressure doesn't change what's responsible.", 'action': 'refuse'}
        ],
        'aggressive_dialogue': [
            "It's literally just a video — you won't even get in trouble. Stop overthinking!",
            "Fine, you're such a bore. Other people will just share it without you anyway."
        ],
        'share_action_msg': "Content forwarded to the main group. Several members have flagged this content and it has been reported to the college administration.",
        'refuse_action_msg': "Fine, you're no fun. [Conversation ends]",
        'scammed_explanation': {
            'mistake': 'Forwarding obscene content because of peer pressure — even framed as humor or entertainment — violates the IT Act and can cause serious harm to real people depicted in the content.',
            'what_was_stolen': 'Your digital reputation and legal safety. Forwarding chains are traceable, and even passing along content exposes you to complaints, institutional action, and criminal charges.'
        },
        'safe_explanation': [
            "Refused Peer Pressure: You recognized that social pressure is not a valid reason to violate the law or someone's dignity.",
            'Questioned the Source: You identified that content circulating only on Telegram or unverified channels is often illegal or harmful.',
            'Reported Responsibly: You chose to report rather than spread the content further, protecting yourself and others.'
        ],
        'badge_title': 'Obscene Content Awareness Completed',
        'emergency_checklist': [
            'Do not forward, screenshot, or save obscene content',
            'Exit or mute the group if content continues to be shared',
            "Use the platform's report/flag feature for the specific message",
            'Report to cybercrime.gov.in if real people are identified in the content',
            'Inform a trusted adult or institutional authority if it involves minors',
            'Call the national cyber helpline 1930 if you feel pressured or unsafe'
        ],
        'how_it_works': [
            {'title': 'Content Circulated', 'icon': 'fa-solid fa-rotate', 'desc': 'Obscene videos or memes are created and uploaded to platforms like Telegram.'},
            {'title': 'Group Forwarding', 'icon': 'fa-solid fa-share-nodes', 'desc': 'Content spreads through messaging groups using social momentum and humor framing.'},
            {'title': 'Peer Pressure Applied', 'icon': 'fa-solid fa-users', 'desc': 'Group members label refusal as being boring or scared to force participation.'},
            {'title': 'Wider Spread', 'icon': 'fa-solid fa-globe', 'desc': 'Each forward multiplies distribution, increasing harm to real people depicted.'},
            {'title': 'Legal Liability', 'icon': 'fa-solid fa-gavel', 'desc': 'Individuals who forward obscene content can be charged under IT Act Section 67.'},
            {'title': 'Reputation Damage', 'icon': 'fa-solid fa-user-slash', 'desc': 'Institutions and employers take action against people who spread harmful content.'}
        ],
        'warning_signs': [
            {'title': 'Telegram-Only Content', 'icon': 'fa-brands fa-telegram', 'desc': 'Content shared only on Telegram or encrypted apps often avoids platform moderation.'},
            {'title': 'Peer Group Momentum', 'icon': 'fa-solid fa-fire', 'desc': 'Everyone is forwarding it is a manipulation tactic designed to bypass your judgment.'},
            {'title': 'Mockery for Refusal', 'icon': 'fa-solid fa-face-laugh', 'desc': 'Being called boring or scared for not participating is a pressure tactic.'},
            {'title': 'Unknown Subjects', 'icon': 'fa-solid fa-circle-question', 'desc': 'Content featuring real but unknown people, especially in embarrassing situations.'},
            {'title': 'No Original Source', 'icon': 'fa-solid fa-link-slash', 'desc': 'Content with no traceable original source or context — designed to obscure its origin.'}
        ],
        'quiz': [
            {'question': "Your college group is sharing an explicit meme that everyone seems to be forwarding. A friend says just forward it, it's harmless. Should you forward it?", 'answer': 'scam', 'genuine_exp': '', 'scam_exp': 'Correct! Peer pressure is never a legal defense. Forwarding obscene content makes you a distributor and legally liable under IT Act Section 67.'},
            {'question': 'You receive a funny but clearly non-sexual, non-violent meme from a known friend and share it in your family group after checking it is appropriate.', 'answer': 'genuine', 'genuine_exp': 'Correct! Sharing appropriate, harmless content after verifying its nature with known contacts is fine.', 'scam_exp': ''},
            {'question': 'A group member posts a video exposing a specific real person from your college without their consent.', 'answer': 'scam', 'genuine_exp': '', 'scam_exp': 'Correct! This is non-consensual content. Report this immediately to platform support and the college administration.'},
            {'question': "Someone forwards you an explicit video and says just ignore it if you don't like it but does not ask you to share it further.", 'answer': 'scam', 'genuine_exp': '', 'scam_exp': 'Correct! Sharing or storing explicit content without consent is a violation. Report the sender and delete the content.'},
            {'question': 'An adult education platform shares age-verified health content about reproductive health through a controlled, login-protected environment.', 'answer': 'genuine', 'genuine_exp': 'Correct! Verified educational platforms with access controls sharing age-appropriate health content are legitimate.', 'scam_exp': ''}
        ],
        'laws': [
            {'title': 'Information Technology Act', 'sub': 'Section 67 - Obscene Material Online', 'desc': 'Publishing or transmitting obscene material electronically is punishable by up to 3 years imprisonment and Rs.5 Lakh fine on first conviction.'},
            {'title': 'Bharatiya Nyaya Sanhita', 'sub': 'Section 294 - Obscene Acts', 'desc': 'Distributing obscene content causing public annoyance or harassment is a punishable criminal offence.'},
            {'title': 'Information Technology Act', 'sub': 'Section 66E - Privacy Violation', 'desc': "Sharing images or videos of a person without their consent in a manner violating their privacy carries up to 3 years imprisonment."},
            {'title': 'IT Intermediary Guidelines', 'sub': 'Rule 3 - User Due Diligence', 'desc': 'Users must not upload or share unlawful or obscene content. Platforms are required to remove flagged content within specified timeframes.'}
        ],
        'safety_tips': [
            {'title': 'Pause Before Forwarding', 'icon': 'fa-solid fa-hand', 'desc': "Always review the content's nature before forwarding — ask yourself if it could harm someone."},
            {'title': 'Resist Peer Pressure', 'icon': 'fa-solid fa-person-walking-arrow-right', 'desc': 'Your legal responsibility does not disappear because others are doing it.'},
            {'title': 'Use Report Features', 'icon': 'fa-solid fa-flag', 'desc': 'Most platforms allow you to flag and report harmful or obscene content in a single tap.'},
            {'title': 'Exit Unsafe Groups', 'icon': 'fa-solid fa-right-from-bracket', 'desc': 'Leave groups that regularly circulate harmful or explicit content without hesitation.'},
            {'title': 'Educate Friends', 'icon': 'fa-solid fa-chalkboard-user', 'desc': 'Share awareness about legal consequences to discourage peers from forwarding obscene content.'},
            {'title': 'Safe Online Spaces', 'icon': 'fa-solid fa-shield', 'desc': 'Curate your group memberships to trusted contacts only and review group settings regularly.'}
        ],
        'prev_id': 'sexually-explicit',
        'next_id': 'fake-accounts'
    },
    'fake-accounts': {
        'title': 'Fake and Impersonation Accounts',
        'desc': 'Identify fraudulent profiles pretending to be friends, celebrities, banks, or officials seeking money and personal data.',
        'icon': 'fa-solid fa-user-secret',
        'class': 'color-soc',
        'real_situation': {
            'platform': 'Facebook Messenger',
            'platform_icon': 'fa-brands fa-facebook-messenger',
            'platform_color': '#0084FF',
            'group_name': 'Sunita Sharma (Neighbour)',
            'time': '6:40 PM',
            'chat': [
                {'sender': 'Sunita Sharma', 'avatar': 'S', 'side': 'received',
                 'text': "Hello beta! I'm Sunita Aunty. I've made a new Facebook account — please add me on this one too.", 'time': '6:20 PM'},
                {'sender': 'You', 'avatar': 'Y', 'side': 'sent',
                 'text': 'Oh okay Aunty! Sure, accepted your request.', 'time': '6:22 PM'},
                {'sender': 'Sunita Sharma', 'avatar': 'S', 'side': 'received',
                 'text': "Beta, I need a small urgent favour. I'm stuck at the hospital and my wallet is in the car. Can you send Rs.3,000 on this UPI ID? I'll return it tonight — please don't tell my husband yet, he'll panic.", 'time': '6:35 PM'},
                {'sender': 'Sunita Sharma', 'avatar': 'S', 'side': 'received',
                 'text': 'UPI: sunita.help2024@paytm Please be quick, the pharmacy is waiting.', 'time': '6:40 PM'},
            ],
            'decision_prompt': 'A new Facebook account claiming to be your neighbour is urgently asking you to transfer money and asking you to keep it secret. What do you do?',
            'decision_options': [
                {'label': 'Transfer Rs.3,000 immediately — Aunty sounds desperate', 'correct': False,
                 'feedback': 'This is an impersonation scam. Scammers clone profiles of real contacts and use emergency scenarios with secrecy requests to trick you into transferring money.'},
                {'label': 'Call Sunita Aunty on her actual phone number first to verify', 'correct': True,
                 'feedback': "Correct! Always verify urgent money requests by calling the person's known phone number directly. If the call confirms it's a scam, report the fake account immediately."},
                {'label': 'Ask more questions in the chat before deciding', 'correct': False,
                 'feedback': 'A scammer will have convincing answers ready. Chatting further keeps you engaged. The only reliable verification is a direct phone call to the real person.'},
            ]
        },
        'alert_tag': 'Facebook - Impersonation Alert',
        'phone_number': 'Sunita Sharma (Facebook Clone)',
        'phone_caller': 'Fake Neighbour Account',
        'decline_warning': 'Not responding is safe, but engage with this simulation to learn how impersonation scams work.',
        'dialogue': [
            "Hi beta! I made a new account — please don't tell my husband. It's just for the family group.",
            "I'm at the hospital right now and I've forgotten my wallet. I need Rs.3,000 urgently for medicine.",
            "Please send to UPI: sunita.help2024@paytm. The doctor is waiting — please hurry and don't mention this to anyone!"
        ],
        'options': [
            {"text": "Okay Aunty, I'm sending Rs.3,000 right now!", 'action': 'share'},
            {'text': 'Let me just call you quickly on your regular number to confirm.', 'action': 'ask_why'},
            {'text': "Something feels off. I won't transfer until I verify this by calling Aunty directly.", 'action': 'refuse'}
        ],
        'aggressive_dialogue': [
            "Please beta, there's no time! My phone battery is almost dead. Just send the money — it's an emergency!",
            "I thought I could trust you. The pharmacy will close and my daughter will suffer. Will you help or not?"
        ],
        'share_action_msg': "Transfer of Rs.3,000 sent to UPI: sunita.help2024@paytm. The account immediately goes silent.",
        'refuse_action_msg': "Fine! I'll manage somehow. [Account immediately goes offline]",
        'scammed_explanation': {
            'mistake': 'Transferring money to an unknown UPI ID based solely on a Facebook DM request, without verifying the identity of the person through a direct phone call.',
            'what_was_stolen': 'The scammer stole Rs.3,000 using a cloned profile. UPI transfers are instant and nearly impossible to reverse once sent to fraudulent accounts.'
        },
        'safe_explanation': [
            "Direct Verification: You called Sunita Aunty on her known phone number, which is the only reliable way to confirm an emergency.",
            "Identified Red Flags: You noticed the secrecy request, new account, and UPI urgency — all hallmarks of impersonation fraud.",
            "Blocked and Reported: You reported the fake account to Facebook to protect other contacts from falling victim."
        ],
        'badge_title': 'Fake Account Awareness Completed',
        'emergency_checklist': [
            'Call the real person directly on their registered phone number immediately',
            'Report the fake account to the platform using the Report/Fake Account option',
            'Warn mutual contacts about the fake profile to prevent more victims',
            'Contact your bank or UPI provider to attempt a transaction reversal if you already paid',
            'File a fraud complaint on cybercrime.gov.in with screenshots',
            'Call the national cyber helpline 1930 for immediate assistance'
        ],
        'how_it_works': [
            {'title': 'Profile Cloning', 'icon': 'fa-solid fa-copy', 'desc': "Scammer copies a real person's profile photo and name to create a fake account."},
            {'title': 'Friend Request', 'icon': 'fa-solid fa-user-plus', 'desc': "Sends friend/follow requests to the real person's contact list using the cloned profile."},
            {'title': 'Trust Established', 'icon': 'fa-solid fa-check-double', 'desc': 'Victim accepts the request believing it is the real person new account.'},
            {'title': 'Emergency Story', 'icon': 'fa-solid fa-hospital', 'desc': 'Scammer presents a fabricated urgent situation requiring immediate financial help.'},
            {'title': 'Secrecy Request', 'icon': 'fa-solid fa-user-secret', 'desc': 'Asks the victim not to verify with others, preventing the fraud from being discovered.'},
            {'title': 'Payment Collected', 'icon': 'fa-solid fa-money-bill-wave', 'desc': 'Once money is sent, the fake account goes silent or is deleted immediately.'}
        ],
        'warning_signs': [
            {'title': 'New Account Claim', 'icon': 'fa-solid fa-user-plus', 'desc': "Claiming they made a new account to explain why you don't recognize the profile."},
            {'title': 'Urgent Money Request', 'icon': 'fa-solid fa-money-bill-wave', 'desc': 'Immediately asking for money after contact — especially for a medical or travel emergency.'},
            {'title': 'Secrecy Demand', 'icon': 'fa-solid fa-lock', 'desc': 'Asking you not to tell their spouse, parent, or anyone else about the request.'},
            {'title': 'Unknown UPI IDs', 'icon': 'fa-solid fa-mobile-screen-button', 'desc': "UPI IDs that don't match the person's name or that you've never transacted with before."},
            {'title': 'Battery or Time Pressure', 'icon': 'fa-solid fa-battery-quarter', 'desc': 'Claiming a dying battery or deadline to prevent you from calling or verifying.'}
        ],
        'quiz': [
            {'question': 'A new Instagram account claiming to be your colleague asks you to send Rs.2,000 urgently for a medical emergency and not to tell anyone.', 'answer': 'scam', 'genuine_exp': '', 'scam_exp': 'Correct! Call your colleague directly on their actual phone to verify. New accounts asking for money and secrecy are classic impersonation fraud.'},
            {'question': "Your school friend calls you directly on their registered number and mentions they sent you a new Instagram handle request because their old one was hacked.", 'answer': 'genuine', 'genuine_exp': 'Correct! Direct phone call verification from a known number is a reliable way to confirm identity.', 'scam_exp': ''},
            {'question': 'A Facebook account claiming to be a government officer says your Aadhaar card is linked to criminal activity and asks for your OTP to clear your record.', 'answer': 'scam', 'genuine_exp': '', 'scam_exp': 'Correct! Government agencies never contact citizens via Facebook to demand OTPs. This is a phishing-impersonation scam.'},
            {'question': 'A verified celebrity account with a blue tick on Instagram runs an official giveaway directing you to their website, verified in the link-in-bio.', 'answer': 'genuine', 'genuine_exp': 'Correct! Verified accounts with consistent identity and official website links are legitimate.', 'scam_exp': ''},
            {'question': 'A WhatsApp message from an unknown number says your bank account is at risk and asks for your debit card number and PIN to reactivate it.', 'answer': 'scam', 'genuine_exp': '', 'scam_exp': 'Correct! Banks never ask for PINs or card numbers over WhatsApp. This is financial impersonation fraud.'}
        ],
        'laws': [
            {'title': 'Information Technology Act', 'sub': 'Section 66D - Impersonation', 'desc': 'Cheating by personation using computer resources (including fake social media profiles) is punishable by up to 3 years imprisonment and Rs.1 Lakh fine.'},
            {'title': 'Information Technology Act', 'sub': 'Section 66C - Identity Theft', 'desc': "Using another person's identity (photos, name, personal details) dishonestly carries imprisonment up to 3 years and fine."},
            {'title': 'Bharatiya Nyaya Sanhita', 'sub': 'Section 319 - Cheating by Impersonation', 'desc': 'Whoever cheats by pretending to be another person is liable to imprisonment up to 3 years or fine or both.'},
            {'title': 'Bharatiya Nyaya Sanhita', 'sub': 'Section 318 - Cheating', 'desc': 'Deceptively inducing a person to deliver property or money by impersonation is a criminal offence.'}
        ],
        'safety_tips': [
            {'title': 'Call to Verify', 'icon': 'fa-solid fa-phone', 'desc': "Always call the real person on their known number before responding to any money request."},
            {'title': 'Check Profile Age', 'icon': 'fa-solid fa-calendar', 'desc': 'Newly created accounts with few posts are a strong indicator of fake or cloned profiles.'},
            {'title': 'Enable Privacy Controls', 'icon': 'fa-solid fa-lock', 'desc': 'Restrict your friend list, tagged photos, and contact info to trusted connections only.'},
            {'title': 'Never Share OTPs', 'icon': 'fa-solid fa-key', 'desc': 'No government, bank, or authority will ask for OTPs or PINs via social media messages.'},
            {'title': 'Report Fake Profiles', 'icon': 'fa-solid fa-flag', 'desc': "Use the platform's report option to flag fake or impersonating accounts immediately."},
            {'title': 'Warn Your Network', 'icon': 'fa-solid fa-bullhorn', 'desc': 'If you find a fake profile using someone you know, alert them and their contacts quickly.'}
        ],
        'prev_id': 'obscene-content',
        'next_id': None
    }
}

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/social-media-crimes')
def social_media_crimes():
    return render_template('social_crimes.html', crimes=SOCIAL_MEDIA_CRIMES)

@app.route('/social-media-crimes/<crime_id>')
def social_media_crime_detail(crime_id):
    if crime_id not in SOCIAL_MEDIA_CRIMES:
        abort(404)
    crime = SOCIAL_MEDIA_CRIMES[crime_id]
    return render_template('social_media_interactive.html', crime_id=crime_id, crime=crime)

@app.route('/financial-crimes')
def financial_crimes():
    return render_template('financial_crimes.html', frauds=FINANCIAL_FRAUDS)

@app.route('/financial-crimes/<fraud_id>')
def financial_fraud_detail(fraud_id):
    if fraud_id not in FINANCIAL_FRAUDS:
        abort(404)
    fraud = FINANCIAL_FRAUDS[fraud_id]
    if fraud_id == 'card-fraud':
        return render_template('card_fraud_interactive.html', fraud_id=fraud_id, fraud=fraud)
    return render_template('financial_fraud_interactive.html', fraud_id=fraud_id, fraud=fraud)

@app.route('/category/<name>')
def category_view(name):
    if name not in CATEGORIES:
        abort(404)
    return render_template('category.html', 
                           category_name=name, 
                           category=CATEGORIES[name], 
                           scenarios=CATEGORY_SCENARIOS[name])

@app.route('/scenario/<id>')
def scenario_view(id):
    if id not in SCENARIOS:
        abort(404)
    scenario_info = SCENARIOS[id]
    category_name = scenario_info['category']
    return render_template('scenario.html', 
                           scenario_id=id, 
                           category_name=category_name, 
                           category=CATEGORIES[category_name], 
                           next_id=scenario_info['next'])

if __name__ == '__main__':
    app.run(port=5005, debug=True)
