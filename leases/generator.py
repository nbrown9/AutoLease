import pandas as pd
import os
from fdfgen import forge_fdf
from leases.lease import Lease
import time
import datetime
from datetime import timedelta
from dateutil.relativedelta import relativedelta


class Generator(object):


    def __init__(self):
        self.df = 0
        self.fields = dict.fromkeys(['Owner', 'Date', 't_name', 't_name2', 'Apartment', 'Unit', 'City', 'Zip', 'child_count', 'lease_length', 
        'start_date', 'end_date', 'Rent', 'pet_fee', 'sec_dep', '2monthrent'])   # Tenant Name        
        self.upload_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'media')
        self.dir_file = os.path.join(self.upload_path, 'broward_reg.pdf')
        self.dir_filwpb = os.path.join(self.upload_path, 'palmbeach_reg.pdf')
        self.dir_filbs = os.path.join(self.upload_path, 'broward_studio.pdf')
        self.dir_filwpbs = os.path.join(self.upload_path, 'palmbeach_studio.pdf')
        self.filenames = []
        
        self.tenantdf = pd.read_csv('tenant_directory.csv', delimiter=',')
        self.unitdf = pd.read_csv('unit_directory.csv', delimiter=',')
    #import the csv file from the media folder it was uploaded to
    def importcsv(self, unitdir):
        self.df = pd.read_csv(unitdir, delimiter=',')

    #uses imported csv to generate the pdf files in a folder called output    
    def generateform(self):
        i = 0;
        filenames = []
        timestring = self.df.loc[i, 'Lease Expires']
        datetime_object = datetime.datetime.strptime(timestring, '%m/%d/%y').date()
        current_time = time.strftime("%m/%d/%Y")
        for row in self.df.values:
            starting_lease_date = datetime_object + datetime.timedelta (days = 1)
            ending_lease_date = starting_lease_date + relativedelta(months = int(self.df.loc[i,'Duration'])) - datetime.timedelta (days = 1)
            name = str(self.df.loc[i, 'Tenant Name'])
            unitzip = self.df.loc[i,'Property Zip']
            wcount = 0
            t_name2 = ''
            for row in self.tenantdf.values:
                if (self.tenantdf.loc[wcount, 'Property'] == self.df.loc[i, 'Property'] and self.tenantdf.loc[wcount, 'Unit'] == self.df.loc[i, 'Unit'] and self.tenantdf.loc[wcount, 'Tenant'] != self.df.loc[i, 'Tenant Name']):
                    t_name2 = self.tenantdf.loc[wcount, 'Tenant']
                wcount = wcount + 1
            wcount2 = 0
            isStudio = False
            for row in self.unitdf.values:
                if self.unitdf.loc[wcount2, 'Bedrooms'] == 0 and self.df.loc[i, 'Property'] == self.unitd.loc[wcount2, 'Property']:
                    isStudio = True
            
            self.fields = [
                ('Owner', self.df.loc[i, 'Owner(s)']), 
                ('Date', current_time), 
                ('T1', self.df.loc[i, 'Tenant Name']),
                ('T2', t_name2),

                ('Add', self.df.loc[i, 'Property Street Address 1']),
                ('Unit', self.df.loc[i,'Unit']),
                ('City', self.df.loc[i,'Property City']),
                ('Zip', self.df.loc[i,'Property Zip']),
                ('child_count', ' '),
                ('Yr', int(self.df.loc[i,'Duration'])),
                ('Start', starting_lease_date.strftime("%m/%d/%Y")),
                ('End', ending_lease_date.strftime("%m/%d/%Y")),
                ('Rent', "%.2f" % self.df.loc[i,'New Rent']),
                ('Pet', '0'),
                ('SD', self.df.loc[i,'Deposit']),
                ('2 months rent', "{0:.2f}".format(self.df.loc[i,'New Rent']*2))]
            fdf = forge_fdf("", self.fields, [], [], [])
            fdf_file = open("data.fdf", "wb")
            fdf_file.write(fdf)
            fdf_file.close()
            #Determines if in palm beach
            if unitzip in {33460,33401,33407,33405,33409}:
                print(self.df.loc[i,'Tenant Name'])
                if isStudio:
                    os.system('pdftk '+self.dir_filwpbs+' fill_form data.fdf output output/'+name.replace(" ","")+'UnsignedLease.pdf flatten')
                if isStudio == False:
                    os.system('pdftk '+self.dir_filwpb+' fill_form data.fdf output output/'+name.replace(" ","")+'UnsignedLease.pdf flatten')
            else:
                if isStudio:
                    os.system('pdftk '+self.dir_filbs+' fill_form data.fdf output output/'+name.replace(" ","")+'UnsignedLease.pdf flatten')
                if isStudio == False:
                    os.system('pdftk '+self.dir_file+' fill_form data.fdf output output/'+name.replace(" ","")+'UnsignedLease.pdf flatten')
            i = i+1
            filenames.append(str(name.replace(" ","")+'UnsignedLease.pdf'))
        self.filenames = filenames
        print self.filenames
    
    #returns the dictionary of uploaded file names
    def createdfiles(self):
        return self.filenames
