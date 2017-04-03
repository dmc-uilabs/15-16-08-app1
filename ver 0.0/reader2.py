#!/usr/bin/python

import psycopg2,datetime

#connecting to the database
try:
    conn="host='152.1.58.206' port=5432 dbname='postgres' user='postgres' password='ssr'"
    con=psycopg2.connect(conn)
    cur=con.cursor()
    connection_status="Connected"
except:
    var=datetime.datetime.now().isoformat()
    var=var.replace(":"," ");var=var.replace("-"," ");
    with open('xaa2.out', 'w') as f:
        f.write("connection_status = No Connection Made\n" )
        f.write("timestamp_current = " + str(var) + "\n" )
        f.write("machine_status = NA\n")
        f.write("timestamp_status_update = NA\n")
        f.write("part_count = 0.00\n")
        f.write("machine_utilization = 0.00\n")
        f.write("OEE = 0.00\n")
        f.write("comment = ERROR Is the server running on host 152.1.58.206 and accepting connections on port 5432")


#input extraction
if connection_status=="Connected":
    input=open('xaa2','r')
    input_init=input.readlines()
    time_period=float(input_init[3][13:(len(input_init[3])-1)])
    if 'HAAS' in input_init[1]:
        machine_name='HAAS-VF2'
    if 'MAZAK' in input_init[1]:
        machine_name='MAZAK-M7303290458'
    
    times=datetime.datetime.now()-datetime.timedelta(hours=time_period)

    timestamp_begin= str(input_init[0][17:(len(input_init[0])-1)])
    timestamp_begin=timestamp_begin.replace(" ","")
    timestamp_begin=timestamp_begin.replace("Y","-")
    timestamp_begin=timestamp_begin.replace("H",":")
    
    timestamp_end= str(input_init[2][15:(len(input_init[2])-1)])
    timestamp_end=timestamp_end.replace(" ","")
    timestamp_end=timestamp_end.replace("Y","-")
    timestamp_end=timestamp_end.replace("H",":")
    


    #query to the database
    if len(timestamp_begin)>3 and len(timestamp_end)>3:
        cur.execute(""" SELECT * from login where machine_name='"""+str(machine_name)+"""' and timestamp>='"""+ str(timestamp_begin)+"""' and timestamp<='"""+ str(timestamp_end)+"""' order by timestamp desc""")
        a=cur.fetchall()
    else:
        cur.execute(""" SELECT * from login where machine_name='"""+str(machine_name)+"""' and timestamp>='"""+ str(times.isoformat())+"""' order by timestamp desc""")
        a=cur.fetchall()     

    time=float(0)
    #calculating machine utilization
    for x in range(0,len(a)):
        if a[x][3]=='OFF':
            try:
                if x!=0 and a[x-1][3]!='OFF':
                    time=time + (datetime.datetime(int(a[x-1][1][0:4]),int(a[x-1][1][5:7]),int(a[x-1][1][8:10]),int(a[x-1][1][11:13]),int(a[x-1][1][14:16]),int(a[x-1][1][17:19]))-datetime.datetime(int(a[x][1][0:4]),int(a[x][1][5:7]),int(a[x][1][8:10]),int(a[x][1][11:13]),int(a[x][1][14:16]),int(a[x][1][17:19]))).total_seconds()
                    #print 'hello'
            except:
                'nothing'
            if x==0 and x!=(len(a)-1):
                if len(timestamp_begin)>3 and len(timestamp_end)>3:
                    time=time + (datetime.datetime(int(timestamp_end[0:4]),int(timestamp_end[5:7]),int(timestamp_end[8:10]),int(timestamp_end[11:13]),int(timestamp_end[14:16]),int(timestamp_end[17:19]))-datetime.datetime(int(a[x][1][0:4]),int(a[x][1][5:7]),int(a[x][1][8:10]),int(a[x][1][11:13]),int(a[x][1][14:16]),int(a[x][1][17:19]))).total_seconds()
                else:
                    time=time + (datetime.datetime.now()-datetime.datetime(int(a[x][1][0:4]),int(a[x][1][5:7]),int(a[x][1][8:10]),int(a[x][1][11:13]),int(a[x][1][14:16]),int(a[x][1][17:19]))).total_seconds()
                #print 'no'
        elif x==(len(a)-1):
            if len(timestamp_begin)>3 and len(timestamp_end)>3:
                aa=timestamp_begin.replace(" ","")
            else:
                aa=times.isoformat()
            time=time+ (datetime.datetime(int(a[x][1][0:4]),int(a[x][1][5:7]),int(a[x][1][8:10]),int(a[x][1][11:13]),int(a[x][1][14:16]),int(a[x][1][17:19]))-datetime.datetime(int(aa[0:4]),int(aa[5:7]),int(aa[8:10]),int(aa[11:13]),int(aa[14:16]),int(aa[17:19]))).total_seconds()
            #print time

    if len(timestamp_begin)>3 and len(timestamp_end)>3:
        rand=(datetime.datetime(int(timestamp_end[0:4]),int(timestamp_end[5:7]),int(timestamp_end[8:10]),int(timestamp_end[11:13]),int(timestamp_end[14:16]),int(timestamp_end[17:19]))-datetime.datetime(int(timestamp_begin[0:4]),int(timestamp_begin[5:7]),int(timestamp_begin[8:10]),int(timestamp_begin[11:13]),int(timestamp_begin[14:16]),int(timestamp_begin[17:19]))).total_seconds()

        machine_utilization=(rand -time)/(rand)/(0.01)

    else:
        machine_utilization=(time_period*3600-time)/float(time_period*36)

    #calculating machine OEE
    time1=0
    for x in range(0,len(a)):
        if a[x][4]=='ACTIVE':
            
            try:
                if x!=0 and a[x-1][4]!='ACTIVE':
                    time1=time1 + (datetime.datetime(int(a[x-1][1][0:4]),int(a[x-1][1][5:7]),int(a[x-1][1][8:10]),int(a[x-1][1][11:13]),int(a[x-1][1][14:16]),int(a[x-1][1][17:19]))-datetime.datetime(int(a[x][1][0:4]),int(a[x][1][5:7]),int(a[x][1][8:10]),int(a[x][1][11:13]),int(a[x][1][14:16]),int(a[x][1][17:19]))).total_seconds()
            except:
                'nothing'
            if x==0 and x!=(len(a)-1):
                if len(timestamp_begin)>3 and len(timestamp_end)>3:
                    time1=time1 + (datetime.datetime(int(timestamp_end[0:4]),int(timestamp_end[5:7]),int(timestamp_end[8:10]),int(timestamp_end[11:13]),int(timestamp_end[14:16]),int(timestamp_end[17:19]))-datetime.datetime(int(a[x][1][0:4]),int(a[x][1][5:7]),int(a[x][1][8:10]),int(a[x][1][11:13]),int(a[x][1][14:16]),int(a[x][1][17:19]))).total_seconds()
                else:
                    time1=time1 + (datetime.datetime.now()-datetime.datetime(int(a[x][1][0:4]),int(a[x][1][5:7]),int(a[x][1][8:10]),int(a[x][1][11:13]),int(a[x][1][14:16]),int(a[x][1][17:19]))).total_seconds()
        
            
    
    if len(timestamp_begin)>3 and len(timestamp_end)>3:
        rand1=(datetime.datetime(int(timestamp_end[0:4]),int(timestamp_end[5:7]),int(timestamp_end[8:10]),int(timestamp_end[11:13]),int(timestamp_end[14:16]),int(timestamp_end[17:19]))-datetime.datetime(int(timestamp_begin[0:4]),int(timestamp_begin[5:7]),int(timestamp_begin[8:10]),int(timestamp_begin[11:13]),int(timestamp_begin[14:16]),int(timestamp_begin[17:19]))).total_seconds()

        OEE=(time1)/(rand1)/float(0.01)

    else:
        OEE=(time1)/float(time_period*36)

    part_count=0
    if len(a)>2:
        try:
            initial_count=float(a[0][5])
        except:
            initial_count=float(a[1][5])

        try:
            last_count=float(a[len(a)-1][5])
        except:
            last_count=float(a[len(a)-2][5])

        part_count=initial_count-last_count
    if len(a)>0:
        var=datetime.datetime.now().isoformat()
        var=var.replace(":"," ");var=var.replace("-"," ");
        var2=a[0][1]
        var2=var2.replace(":"," ");var2=var2.replace("-"," ");
        with open('xaa2.out', 'w') as f:
            f.write("connection_status = Connected\n" )
            f.write("timestamp_current = " + str(var) + "\n" )
            f.write("machine_status = "+a[0][3]+"\n")
            f.write("timestamp_status_update = "+str(var2)+"\n")
            f.write("part_count = "+str(part_count)+"\n")
            f.write("machine_utilization = " +str(machine_utilization)+"\n")
            f.write("OEE = " +str(OEE)+"\n")
            f.write("comment = Successful Execution")
    else:
        var=datetime.datetime.now().isoformat()
        var=var.replace(":"," ");var=var.replace("-"," ");
        with open('xaa2.out', 'w') as f:
            f.write("connection_status = Connected\n" )
            f.write("timestamp_current = " + str(var) + "\n" )
            f.write("machine_status = NA\n")
            f.write("timestamp_status_update = NA\n")
            f.write("part_count = 0.00\n")
            f.write("machine_utilization = 0.00\n")
            f.write("OEE = 0.00\n")
            f.write("comment = No data found for the given set of inputs")
       







