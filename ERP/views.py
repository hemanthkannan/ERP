from django.shortcuts import render
import pandas as pd
from django.apps import apps
from django.http import HttpResponse
from django.template import loader
from django.template.loader import get_template
from django.template import Context
import inflect
from datetime import datetime


def LR_VIEW(request):
     # Path to your Excel file
    excel_file_path = 'media/salary.xlsx'
    
    # Read the Excel file into a Pandas DataFrame
    df = pd.read_excel(excel_file_path)
    

    # Convert DataFrame records to a list of dictionaries
    records = df.to_dict(orient='records')
    

    # Pass the records to the template context
    context = {
        'records': records,
    }

    return render(request,'LR.html',context)

def invoice_view(request):
    print("here")
     # Path to your Excel file
    excel_file_path = 'media/invoice.xlsx'
    
    # Read the Excel file into a Pandas DataFrame
    df = pd.read_excel(excel_file_path)
    df=df.fillna('')

    # Convert DataFrame records to a list of dictionaries
    records = df.to_dict(orient='records')
    

    # Pass the records to the template context
    context = {
        'records': records,
    }
    return render(request, 'invoice.html',context)

def read_excel():
    excel_file_path = 'media/invoice1.xlsx'
    df = pd.read_excel(excel_file_path)
    return df

def number_to_words(number):
    p = inflect.engine()
    words = p.number_to_words(number,andword="and")
    words = words.replace(',', '')  # Remove the comma
    return words

def tax_invoice_form(request):

    # Access the DataFrame defined in AppConfig
    your_app_config = apps.get_app_config('ERP')
    df = your_app_config.df
    print('INGA)))))))))))((((((((((()))))))))))',df)

    # Use 'df' as needed in your view logic
    # ...

    global Company_name
    global From_date
    global To_date
    global Filtered_df_first_submission
    
    #print(df)
    if request.method == 'POST':
        if 'fetch' in request.POST:
            print('HERE3')
            company_name = request.POST.get('company')
            from_date = request.POST.get('from_date')
            to_date = request.POST.get('to_date')
            Company_name=company_name
            From_date=from_date
            To_date=to_date

            filtered_df = df[(df['Company'] == company_name) & (df['lr_hire_date']>=from_date) & (df['lr_hire_date']<=to_date)]
            
            print('filtered_df----->',filtered_df)
            Filtered_df_first_submission=filtered_df
            freight_billed_to = Filtered_df_first_submission['to_branch'].unique()
            shipped_from = Filtered_df_first_submission['from_branch'].unique()

            print('freight_billed_to----->',freight_billed_to)
            print('shipped_from----->',shipped_from)
            
            context = {
                        'freight_billed_to': freight_billed_to,
                        'shipped_from': shipped_from,
                        'company_name':company_name
                        }
            return render(request, 'Tax_invoice_form.html',context)

        if 'invoice_print' in request.POST:

            freight_billed_to= request.POST.get('freight')
            shipped_from= request.POST.get('shipped_from')
            GST_selection = request.POST.get('GSTselection')
            Invoice_number = request.POST.get('invoiceNumber')
            dateInput = request.POST.get('dateInput')
            SOS_selection = request.POST.get('GST-supplyofsrevice-selection')
            
            df=Filtered_df_first_submission

            filtered_df = df[(df['from_branch']==shipped_from) & (df['to_branch']==freight_billed_to)]

            df2=filtered_df.groupby(['Company','gdm_no','lr_hire_date','lr_number','lorry_reg_number','LR_party_invoice','from_branch','to_branch','LR_no_of_packages','LR_weight','consignor_addr','from_city','consignor_pincode','consignor_state','consignee_addr','to_city','consignee_pincode','consignee_state','consignee_gstin','consignor_gstin'])['LR_Rate'].unique().reset_index().explode('LR_Rate')
            df3=df2.groupby(['Company','gdm_no','lr_hire_date','lr_number','lorry_reg_number','from_branch','to_branch','LR_weight','LR_Rate','consignor_addr','from_city','consignor_pincode','consignor_state','consignee_addr','to_city','consignee_pincode','consignee_state','consignee_gstin','consignor_gstin']).agg({'LR_no_of_packages':'sum'}).reset_index()
            df4=df3[['Company','gdm_no','from_branch','to_branch','lr_hire_date','lr_number','lorry_reg_number','LR_no_of_packages','LR_weight','LR_Rate','consignor_addr','from_city','consignor_pincode','consignor_state','consignee_addr','to_city','consignee_pincode','consignee_state','consignee_gstin','consignor_gstin']]

            df4['S_NO']=df4['s.no'] = range(1, len(df4) + 1)
            df4['stat_chg']=15.00
            df4['total_amount']=round((df4["LR_weight"]*df4["LR_Rate"])+df4["stat_chg"])


            #df4.to_excel('sdfsd.xlsx')
            consignor_gstin=df4['consignor_gstin'].unique()[0]
            consignor_addr=df4['consignor_addr'].unique()[0]
            consignor_pincode=df4['consignor_pincode'].unique()[0]
            consignor_state=df4['consignor_state'].unique()[0].upper()
            from_city=df4['from_city'].unique()[0]

            consignee_gstin=df4['consignee_gstin'].unique()[0]
            consignee_addr=df4['consignee_addr'].unique()[0]
            consignee_pincode=df4['consignee_pincode'].unique()[0]
            consignee_state=df4['consignee_state'].unique()[0].upper()
            to_city=df4['to_city'].unique()[0]

            consignor_addr_combined=consignor_addr.upper()+" "+from_city.upper()+" "+consignor_pincode
            consignee_addr_combined=consignee_addr.upper()+" "+to_city.upper()+" "+consignee_pincode

            df4['LR_weight']=df4['LR_weight'].astype(int)
            df4['total_amount']=df4['total_amount'].astype(int)
            LR_no_of_packages=df4['LR_no_of_packages'].sum()
            LR_weight=df4['LR_weight'].sum()
            total_amount=df4['total_amount'].sum()
            Initial_total_amount=total_amount

            

            if GST_selection=='Withinstate':
                CGST_RATE='2.5%'
                SGST_RATE='2.5%'
                CGST_AMOUNT=(2.5/100)*total_amount
                CGST_AMOUNT=round(CGST_AMOUNT,2)

                SGST_AMOUNT=(2.5/100)*total_amount
                SGST_AMOUNT=round(CGST_AMOUNT,2)

                TOTAL_AMOUNT_GST=CGST_AMOUNT+SGST_AMOUNT
                IGST_RATE=''
                IGST_AMOUNT=''

                GST_word_expand=number_to_words_indian(TOTAL_AMOUNT_GST)


            elif GST_selection=='Outsidestate':
                IGST_RATE='5%'
                IGST_AMOUNT=(5/100)*total_amount
                IGST_AMOUNT=round(IGST_AMOUNT,2)
                TOTAL_AMOUNT_GST=IGST_AMOUNT
                print('---------------->looping',TOTAL_AMOUNT_GST)
                GST_word_expand=number_to_words_indian(TOTAL_AMOUNT_GST)
                CGST_RATE=''
                SGST_RATE=''
                CGST_AMOUNT=''
                SGST_AMOUNT=''
            else:
                print("the selection ofGST was not done")

        
            if SOS_selection=='FCM':
                print('---------------->',SOS_selection)
                print('---------------->',TOTAL_AMOUNT_GST)
                total_amount=total_amount+TOTAL_AMOUNT_GST
                print('here**********',total_amount)
            elif SOS_selection=='RCM':
                total_amount=total_amount
            else:
                print("select the suply of service")


            Prepared_by = request.POST.get('prepared_by')


            final_df=df4[['S_NO','lr_hire_date','lr_number','lorry_reg_number','LR_no_of_packages','LR_weight','LR_Rate','stat_chg','total_amount']]
            # Convert DataFrame records to a list of dictionaries
            final_df['lr_hire_date'] = pd.to_datetime(final_df['lr_hire_date'])
            final_df['lr_hire_date'] = final_df['lr_hire_date'].dt.strftime('%d-%m-%Y')
            final_df['LR_Rate']=final_df['LR_Rate'].map("{:.2f}".format)
            final_df['total_amount']=final_df['total_amount'].map("{:.2f}".format)
            
            total_amount=round(total_amount)
            print('**************',total_amount)
            # Example usage:
            #number = 452454
            word_expand = number_to_words_indian(total_amount)
            total_amount = "{:.2f}".format(total_amount)
            
           

            final_df['stat_chg']=final_df['stat_chg'].map("{:.2f}".format)
            
            records = final_df.to_dict(orient='records')

            if df4['Company'].unique()[0]=='Sreeman':
                Company_Name_Display='SREEMAN TRANSPORTS'
                Account_No='560371000618063'
            elif df4['Company'].unique()[0]=='Suriya':
                Company_Name_Display='SURIYA CARRIERS'
                Account_No='560371000618087'
            else:
                print('Company not listed')

            # Parse the input date string
            date_obj = datetime.strptime(dateInput, "%Y-%m-%d")
            # Format the date object in the desired format
            desired_format = "%d-%m-%Y"
            formatted_date = date_obj.strftime(desired_format)
            print('---------------->after loopinglooping',IGST_AMOUNT)
            print('---------------->after loopinglooping',IGST_RATE)
            
            var=TOTAL_AMOUNT_GST
            rounder_var=round(var)
            round_off_data=round(rounder_var-var,2)

            context = { 
                        'freight_billed_to': freight_billed_to,
                        'shipped_from': shipped_from,
                        'company_name':Company_name,
                        'records':records,
                        'Invoice_number':Invoice_number,
                        'formatted_date':formatted_date,
                        'consignor_gstin':consignor_gstin,
                        'consignee_gstin':consignee_gstin,
                        'consignor_addr_combined':consignor_addr_combined,
                        'consignee_addr_combined':consignee_addr_combined,
                        'consignor_state':consignor_state,
                        'consignee_state':consignee_state,
                        'LR_no_of_packages':LR_no_of_packages,
                        'LR_weight':LR_weight,
                        'Initial_total_amount':Initial_total_amount,
                        'total_amount':total_amount,
                        'word_expand':word_expand,
                        'CGST_RATE':CGST_RATE,
                        'CGST_AMOUNT':CGST_AMOUNT,
                        'SGST_RATE':SGST_RATE,
                        'SGST_AMOUNT':SGST_AMOUNT,
                        'IGST_RATE':IGST_RATE,
                        'IGST_AMOUNT':IGST_AMOUNT,
                        'TOTAL_AMOUNT_GST':TOTAL_AMOUNT_GST,
                        'GST_word_expand':GST_word_expand,
                        'round_off_data':round_off_data,
                        'Company_Name_Display':Company_Name_Display,
                        'Account_No':Account_No,
                        'Prepared_by':Prepared_by,
                        'SOS_selection':SOS_selection,
                        'GST_selection':GST_selection
                        }


            return render(request, 'invoice.html',context)

        

    return render(request, 'Tax_invoice_form.html')


def number_to_words_indian(number):
    units = ["", "one", "two", "three", "four", "five", "six", "seven", "eight", "nine"]
    teens = ["ten", "eleven", "twelve", "thirteen", "fourteen", "fifteen", "sixteen", "seventeen", "eighteen", "nineteen"]
    tens = ["", "", "twenty", "thirty", "forty", "fifty", "sixty", "seventy", "eighty", "ninety"]

    def convert_integer_part(number):
        words = []
        if number >= 10000000:
            crores = number // 10000000
            words.extend(convert_integer_part(crores))
            words.append("crore")
            number %= 10000000
        if number >= 100000:
            lakhs = number // 100000
            words.extend(convert_integer_part(lakhs))
            words.append("lakh")
            number %= 100000
        if number >= 1000:
            thousands = number // 1000
            words.extend(convert_integer_part(thousands))
            words.append("thousand")
            number %= 1000
        if number >= 100:
            hundreds = number // 100
            words.append(units[hundreds])
            words.append("hundred")
            number %= 100
        if number > 0:
            if number < 20:
                words.append(units[number])
            else:
                words.append(tens[number // 10])
                if number % 10 > 0:
                    words.append(units[number % 10])
        return words

    def convert_decimal_part(number):
        words = []
        decimal_digits = str(number).split(".")[1] if "." in str(number) else "0"
        if decimal_digits != "00" and decimal_digits != "0":
            words.append("and")
            decimal_in_words = convert_integer_part(int(decimal_digits))
            words.extend(decimal_in_words)
            words.append("paise")
        return words

    words = []
    integer_part, decimal_part = str(number).split(".") if "." in str(number) else (str(number), "0")
    words.extend(convert_integer_part(int(integer_part)))
    if decimal_part:  # Check if a decimal part exists
        words.extend(convert_decimal_part(float("0." + decimal_part)))

    return " ".join(words).capitalize() + " only"



def print_invoice(request,context):

    return render(request, 'invoice.html',context)
    

def check(request):
    friend = "hi"
    context = {'friend': friend}

    return render(request, 'check.html',context)