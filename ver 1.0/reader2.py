#linux: /usr/bin/python

import psycopg2,datetime

#read the file
inputfile=open('xaa2','r')
inputdict={}
inputlines=inputfile.readlines()
for x in inputlines:
    x=x.strip('\n')
    a=x.split(' = ')
    inputdict[a[0]]=a[1]
  
#connecting to the database
try:
    conn="host='"+str(inputdict['ipaddress_in'])+"' port="+str(inputdict['port_in'])+" dbname='"+str(inputdict['dbname_in'])+"' user='"+str(inputdict['username_in'])+"' password='"+str(inputdict['password_in'])+"'"
    con=psycopg2.connect(conn)
    
    cur=con.cursor()
    connection="Success"
    timestamp_begin=str(inputdict['start_in'])
    
    timestamp_end=str(inputdict['end_in'])
    con.rollback()
    
    if len(timestamp_begin)>3 and len(timestamp_end)>3:
                      
        cur.execute(""" SELECT * from machine_status where machine_name='"""+str(inputdict['machine_name_in'])+"""' and timestamp>='"""+ str(timestamp_begin)+"""' and timestamp<='"""+ str(timestamp_end)+"""' order by timestamp desc""")
        a=cur.fetchall()
        #print(a)

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

    #last update
    var2=a[0][1]
    #time period

    aaa=datetime.datetime.strptime(str(inputdict['start_in']),'%Y-%m-%dT%H:%M:%S')
    bbb=datetime.datetime.strptime(str(inputdict['end_in']),'%Y-%m-%dT%H:%M:%S')
    ccc=bbb-aaa
    time_period=str(float(ccc.days*86400 + ccc.seconds)/3600)
    
    

    
    if True:
        with open('xaa2.out', 'w') as f:
            f.write("""outputTemplate = <!DOCTYPE html> <html>   <head>     <title>Page 1</title>     <link href="https://s3.amazonaws.com/dmdiidome/jquery-ui-themes.css" type="text/css" rel="stylesheet"/>     <link href="https://s3.amazonaws.com/dmdiidome/axure_rp_page.css" type="text/css" rel="stylesheet"/>     <link href="https://s3.amazonaws.com/dmdiidome/stylesd.css" type="text/css" rel="stylesheet"/>     <link href="https://s3.amazonaws.com/dmdiidome/styles.css" type="text/css" rel="stylesheet"/>      </head>      <body>     <div id="base" class="">        <!-- Box1 (Rectangle) -->       <div id="u0" class="ax_default box_1" data-label="Box1">         <div id="u0_div" class=""></div>         <!-- Unnamed () -->         <div id="u1" class="text" style="display:none; visibility: hidden">           <p><span></span></p>         </div>       </div>        <!-- Box2 (Rectangle) -->       <div id="u2" class="ax_default box_1" data-label="Box2">         <div id="u2_div" class=""></div>         <!-- Unnamed () -->         <div id="u3" class="text" style="display:none; visibility: hidden">           <p><span></span></p>         </div>       </div>        <!-- IP Address (Text Field) Parameter ipaddress-->       <div id="u4" class="ax_default text_field" data-label="IP Address">         <input id="ipaddress_out" type="text" placeholder="{{ipaddress_out}}" />       </div> 	  <br />       <!-- PORT (Text Field) Parameter port-->       <div id="u5" class="ax_default text_field" data-label="PORT">         <input id="port_out" type="text" placeholder="{{port_out}}" size="5"/>       </div>        <!-- IP Address (Rectangle) -->       <div id="u6" class="ax_default box_1" data-label="IP Address">         <div id="u6_div" class=""></div>         <!-- Unnamed () -->         <div id="u7" class="text">           <p><span>IP Address:</span></p>         </div>       </div>        <!-- DB Name (Rectangle) -->       <div id="u8" class="ax_default box_1" data-label="DB Name">         <div id="u8_div" class=""></div>         <!-- Unnamed () -->         <div id="u9" class="text">           <p><span>DB Name:</span></p>         </div>       </div>        <!-- User Name (Rectangle) -->       <div id="u10" class="ax_default box_1" data-label="User Name">         <div id="u10_div" class=""></div>         <!-- Unnamed () -->         <div id="u11" class="text">           <p><span>User Name:</span></p>         </div>       </div>        <!-- Password (Rectangle) -->       <div id="u12" class="ax_default box_1" data-label="Password">         <div id="u12_div" class=""></div>         <!-- Unnamed () -->         <div id="u13" class="text">           <p><span>Password:</span></p>         </div>       </div>        <!-- Machine Name (Rectangle) -->       <div id="u14" class="ax_default box_1" data-label="Machine Name">         <div id="u14_div" class=""></div>         <!-- Unnamed () -->         <div id="u15" class="text">           <p><span>Machine Name:</span></p>         </div>       </div>        <!-- Start Time (Rectangle) -->       <div id="u16" class="ax_default box_1" data-label="Start Time">         <div id="u16_div" class=""></div>         <!-- Unnamed () -->         <div id="u17" class="text">           <p><span>Start Time:</span></p>         </div>       </div>        <!-- End Time (Rectangle) -->       <div id="u18" class="ax_default box_1" data-label="End Time">         <div id="u18_div" class=""></div>         <!-- Unnamed () -->         <div id="u19" class="text">           <p><span>End Time:</span></p>         </div>       </div>        <!-- Export Location (Rectangle) -->       <div id="u20" class="ax_default box_1" data-label="Export Location">         <div id="u20_div" class=""></div>         <!-- Unnamed () -->         <div id="u21" class="text">           <p><span>Export Location</span></p>         </div>       </div>        <!-- DB Name (Text Field) parameter dbname-->       <div id="u22" class="ax_default text_field" data-label="DB Name">         <input id="dbname_out" type="text" placeholder="{{dbname_out}}"/>       </div>        <!-- User Name (Text Field) param username -->       <div id="u23" class="ax_default text_field" data-label="User Name">         <input id="username_out" type="text" placeholder="{{username_out}}"/>       </div>        <!-- Password (Text Field) param password -->       <div id="u24" class="ax_default text_field" data-label="Password">         <input id="password_out" type="text" placeholder="{{password_out}}"/>       </div>        <!-- Start Time (Text Field) param start-->       <div id="u25" class="ax_default text_field" data-label="Start Time">         <input id="start_out" type="text" placeholder="{{start_out}}"/>       </div>        <!-- End Time (Text Field) param end-->       <div id="u26" class="ax_default text_field" data-label="End Time">         <input id="end_out" type="text" placeholder="{{end_out}}"/>       </div>        <!-- Machine Name (Droplist) -->       <div id="u27" class="ax_default droplist" data-label="Machine Name">         <select id="machine_name_out" class="selectpicker form-control">           <option value="BM-098-38CG-0311">BM-098-38CG-0311</option>           <option value="HAAS-VF2">HAAS-VF2</option>           <option value="MAZAK-M7303290458">MAZAK-M7303290458</option>         </select>       </div>        <!-- Retrieve Full Dataset (Checkbox) -->       <div id="u28" class="ax_default checkbox" data-label="Retrieve Full Dataset">         <label for="u28_input">           <!-- Unnamed () -->           <div id="u29" class="text">             <p><span>Retrieve Full Dataset</span></p>           </div>         </label>         <input type='checkbox' id='ret_full_dataset_out' onclick='$(this).attr("value", this.checked ? 1 : 0)' value='0'/>       </div>        <!-- Snapshot View (Checkbox) -->       <div id="u30" class="ax_default checkbox" data-label="Snapshot View">         <label for="u30_input">           <!-- Unnamed () -->           <div id="u31" class="text">             <p><span>Snapshot View</span></p>           </div>         </label>         <input type='checkbox' id='snap_view_out' onclick='$(this).attr("value", this.checked ? 1 : 0)' value='0'/>       </div>        <!-- AWS Location (Text Field) param location -->       <div id="u32" class="ax_default text_field" data-label="AWS Location">         <input id="location_out" type="text" value="{{location_out}}"/>       </div>        <!-- Heading (Rectangle) -->       <div id="u33" class="ax_default heading_1" data-label="Heading">         <div id="u33_div" class=""></div>         <!-- Unnamed () -->         <div id="u34" class="text">           <p><span>Machine Sensor Data</span></p>         </div>       </div>        <!-- Connection Status (Text Field) param connection-->       <div id="u35" class="ax_default text_field" data-label="Connection Status">         <input id="connection_out" type="text" placeholder="{{connection_out}}"/>       </div>        <!-- Machine Name (Text Field) param machine_name-->       <div id="u36" class="ax_default text_field" data-label="Machine Name">         <input id="machine_name_out_out" type="text" placeholder="{{machine_name_out_out}}"/>       </div>        <!-- Time Period (Text Field) param time_period-->       <div id="u37" class="ax_default text_field" data-label="Time Period">         <input id="time_period_out" type="text" placeholder="{{time_period_out}}"/>       </div>        <!-- Data Points (Text Field) param data_points-->       <div id="u38" class="ax_default text_field" data-label="machine_status_out">         <input id="machine_status_out" type="text" placeholder="{{machine_status_out}}"/>       </div>        <!-- Ampere (Text Field) param current-->       <div id="u39" class="ax_default text_field" data-label="timestamp_status_update_out">         <input id="timestamp_status_update_out" type="text" placeholder="{{timestamp_status_update_out}}"/>       </div>        <!-- x (Text Field) param accx-->       <div id="u40" class="ax_default text_field" data-label="part_count_out">         <input id="part_count_out" type="text" placeholder="{{part_count_out}}"/>       </div>        <!-- y (Text Field) param accy-->       <div id="u41" class="ax_default text_field" data-label="machine_utilization_out">         <input id="machine_utilization_out" type="text" placeholder="{{machine_utilization_out}}"/>       </div>        <!-- z (Text Field) param accz-->       <div id="u42" class="ax_default text_field" data-label="oee_out">         <input id="oee_out" type="text" placeholder="{{oee_out}}"/>       </div>        <!-- comment (Text Field) param comment-->       <div id="u43" class="ax_default text_field" data-label="comment">         <input id="comment_out" type="text" value="{{comment_out}}"/>       </div>        <!-- Connection Status (Rectangle) -->       <div id="u44" class="ax_default box_1" data-label="Connection Status">         <div id="u44_div" class=""></div>         <!-- Unnamed () -->         <div id="u45" class="text">           <p><span>Connection Status:</span></p>         </div>       </div>        <!-- Machine Name (Rectangle) -->       <div id="u46" class="ax_default box_1" data-label="Machine Name">         <div id="u46_div" class=""></div>         <!-- Unnamed () -->         <div id="u47" class="text">           <p><span>Machine Name:</span></p>         </div>       </div>        <!-- Time Period (Rectangle) -->       <div id="u48" class="ax_default box_1" data-label="Time Period">         <div id="u48_div" class=""></div>         <!-- Unnamed () -->         <div id="u49" class="text">           <p><span>Time Period (hours):</span></p>         </div>       </div>        <!-- Data Points (Rectangle) -->       <div id="u50" class="ax_default box_1" data-label="Data Points">         <div id="u50_div" class=""></div>         <!-- Unnamed () -->         <div id="u51" class="text">           <p><span>Machine Status:</span></p>         </div>       </div>        <!-- Ampere (Rectangle) -->       <div id="u52" class="ax_default box_1" data-label="Ampere">         <div id="u52_div" class=""></div>         <!-- Unnamed () -->         <div id="u53" class="text">           <p><span>Last Status Update:</span></p>         </div>       </div>        <!-- x (Rectangle) -->       <div id="u54" class="ax_default box_1" data-label="x">         <div id="u54_div" class=""></div>         <!-- Unnamed () -->         <div id="u55" class="text">           <p><span>Part Count:</span></p>         </div>       </div>        <!-- y (Rectangle) -->       <div id="u56" class="ax_default box_1" data-label="y">         <div id="u56_div" class=""></div>         <!-- Unnamed () -->         <div id="u57" class="text">           <p><span>Machine Utilization (%):</span></p>         </div>       </div>        <!-- z (Rectangle) -->       <div id="u58" class="ax_default box_1" data-label="z">         <div id="u58_div" class=""></div>         <!-- Unnamed () -->         <div id="u59" class="text">           <p><span>OEE (%):</span></p>         </div>       </div>        <!-- Comment (Rectangle) -->       <div id="u60" class="ax_default box_1" data-label="Comment">         <div id="u60_div" class=""></div>         <!-- Unnamed () -->         <div id="u61" class="text">           <p><span>Comment:</span></p>         </div>       </div>             </div>   </body> </html>    """)
            f.write("\n")
            f.write("connection_out = "+str(connection)+"\n" )
            f.write("machine_name_out_out = " + str(inputdict['machine_name_in']) + "\n" )
            f.write("machine_name_out = "+ str(inputdict['machine_name_in']) + "\n" )
            f.write("time_period_out = "+ str(time_period) + " \n")
            f.write("machine_status_out = "+str(a[0][3])+"\n")
            f.write("timestamp_status_update_out = "+str(var2)+"\n")
            f.write("part_count_out = "+str(part_count)+"\n")
            f.write("machine_utilization_out = "+str(machine_utilization)+"\n")
            f.write("oee_out = "+str(OEE)+"\n")
            f.write("location_out= NA\n")
            f.write("comment_out = Execution successful!\n")
            f.write("ipaddress_out = "+str(inputdict['ipaddress_in'])+"\n")
            f.write("port_out = "+str(inputdict['port_in'])+"\n")
            f.write("dbname_out = "+str(inputdict['dbname_in'])+"\n")
            f.write("username_out = "+str(inputdict['username_in'])+"\n")
            f.write("password_out = XXXXX\n")
            f.write("start_out = "+str(inputdict['start_in'])+"\n")
            f.write("end_out = "+str(inputdict['end_in'])+"\n")
            f.write("ret_full_dataset_out = 0.0\n")
            f.write("snap_view_out = 0.0\n")
                      

except:
    with open('xaa2.out', 'w') as f:
        f.write("""outputTemplate = <!DOCTYPE html> <html>   <head>     <title>Page 1</title>     <link href="https://s3.amazonaws.com/dmdiidome/jquery-ui-themes.css" type="text/css" rel="stylesheet"/>     <link href="https://s3.amazonaws.com/dmdiidome/axure_rp_page.css" type="text/css" rel="stylesheet"/>     <link href="https://s3.amazonaws.com/dmdiidome/stylesd.css" type="text/css" rel="stylesheet"/>     <link href="https://s3.amazonaws.com/dmdiidome/styles.css" type="text/css" rel="stylesheet"/>      </head>      <body>     <div id="base" class="">        <!-- Box1 (Rectangle) -->       <div id="u0" class="ax_default box_1" data-label="Box1">         <div id="u0_div" class=""></div>         <!-- Unnamed () -->         <div id="u1" class="text" style="display:none; visibility: hidden">           <p><span></span></p>         </div>       </div>        <!-- Box2 (Rectangle) -->       <div id="u2" class="ax_default box_1" data-label="Box2">         <div id="u2_div" class=""></div>         <!-- Unnamed () -->         <div id="u3" class="text" style="display:none; visibility: hidden">           <p><span></span></p>         </div>       </div>        <!-- IP Address (Text Field) Parameter ipaddress-->       <div id="u4" class="ax_default text_field" data-label="IP Address">         <input id="ipaddress_out" type="text" placeholder="{{ipaddress_out}}" />       </div> 	  <br />       <!-- PORT (Text Field) Parameter port-->       <div id="u5" class="ax_default text_field" data-label="PORT">         <input id="port_out" type="text" placeholder="{{port_out}}" size="5"/>       </div>        <!-- IP Address (Rectangle) -->       <div id="u6" class="ax_default box_1" data-label="IP Address">         <div id="u6_div" class=""></div>         <!-- Unnamed () -->         <div id="u7" class="text">           <p><span>IP Address:</span></p>         </div>       </div>        <!-- DB Name (Rectangle) -->       <div id="u8" class="ax_default box_1" data-label="DB Name">         <div id="u8_div" class=""></div>         <!-- Unnamed () -->         <div id="u9" class="text">           <p><span>DB Name:</span></p>         </div>       </div>        <!-- User Name (Rectangle) -->       <div id="u10" class="ax_default box_1" data-label="User Name">         <div id="u10_div" class=""></div>         <!-- Unnamed () -->         <div id="u11" class="text">           <p><span>User Name:</span></p>         </div>       </div>        <!-- Password (Rectangle) -->       <div id="u12" class="ax_default box_1" data-label="Password">         <div id="u12_div" class=""></div>         <!-- Unnamed () -->         <div id="u13" class="text">           <p><span>Password:</span></p>         </div>       </div>        <!-- Machine Name (Rectangle) -->       <div id="u14" class="ax_default box_1" data-label="Machine Name">         <div id="u14_div" class=""></div>         <!-- Unnamed () -->         <div id="u15" class="text">           <p><span>Machine Name:</span></p>         </div>       </div>        <!-- Start Time (Rectangle) -->       <div id="u16" class="ax_default box_1" data-label="Start Time">         <div id="u16_div" class=""></div>         <!-- Unnamed () -->         <div id="u17" class="text">           <p><span>Start Time:</span></p>         </div>       </div>        <!-- End Time (Rectangle) -->       <div id="u18" class="ax_default box_1" data-label="End Time">         <div id="u18_div" class=""></div>         <!-- Unnamed () -->         <div id="u19" class="text">           <p><span>End Time:</span></p>         </div>       </div>        <!-- Export Location (Rectangle) -->       <div id="u20" class="ax_default box_1" data-label="Export Location">         <div id="u20_div" class=""></div>         <!-- Unnamed () -->         <div id="u21" class="text">           <p><span>Export Location</span></p>         </div>       </div>        <!-- DB Name (Text Field) parameter dbname-->       <div id="u22" class="ax_default text_field" data-label="DB Name">         <input id="dbname_out" type="text" placeholder="{{dbname_out}}"/>       </div>        <!-- User Name (Text Field) param username -->       <div id="u23" class="ax_default text_field" data-label="User Name">         <input id="username_out" type="text" placeholder="{{username_out}}"/>       </div>        <!-- Password (Text Field) param password -->       <div id="u24" class="ax_default text_field" data-label="Password">         <input id="password_out" type="text" placeholder="{{password_out}}"/>       </div>        <!-- Start Time (Text Field) param start-->       <div id="u25" class="ax_default text_field" data-label="Start Time">         <input id="start_out" type="text" placeholder="{{start_out}}"/>       </div>        <!-- End Time (Text Field) param end-->       <div id="u26" class="ax_default text_field" data-label="End Time">         <input id="end_out" type="text" placeholder="{{end_out}}"/>       </div>        <!-- Machine Name (Droplist) -->       <div id="u27" class="ax_default droplist" data-label="Machine Name">         <select id="machine_name_out" class="selectpicker form-control">           <option value="BM-098-38CG-0311">BM-098-38CG-0311</option>           <option value="HAAS-VF2">HAAS-VF2</option>           <option value="MAZAK-M7303290458">MAZAK-M7303290458</option>         </select>       </div>        <!-- Retrieve Full Dataset (Checkbox) -->       <div id="u28" class="ax_default checkbox" data-label="Retrieve Full Dataset">         <label for="u28_input">           <!-- Unnamed () -->           <div id="u29" class="text">             <p><span>Retrieve Full Dataset</span></p>           </div>         </label>         <input type='checkbox' id='ret_full_dataset_out' onclick='$(this).attr("value", this.checked ? 1 : 0)' value='0'/>       </div>        <!-- Snapshot View (Checkbox) -->       <div id="u30" class="ax_default checkbox" data-label="Snapshot View">         <label for="u30_input">           <!-- Unnamed () -->           <div id="u31" class="text">             <p><span>Snapshot View</span></p>           </div>         </label>         <input type='checkbox' id='snap_view_out' onclick='$(this).attr("value", this.checked ? 1 : 0)' value='0'/>       </div>        <!-- AWS Location (Text Field) param location -->       <div id="u32" class="ax_default text_field" data-label="AWS Location">         <input id="location_out" type="text" value="{{location_out}}"/>       </div>        <!-- Heading (Rectangle) -->       <div id="u33" class="ax_default heading_1" data-label="Heading">         <div id="u33_div" class=""></div>         <!-- Unnamed () -->         <div id="u34" class="text">           <p><span>Machine Sensor Data</span></p>         </div>       </div>        <!-- Connection Status (Text Field) param connection-->       <div id="u35" class="ax_default text_field" data-label="Connection Status">         <input id="connection_out" type="text" placeholder="{{connection_out}}"/>       </div>        <!-- Machine Name (Text Field) param machine_name-->       <div id="u36" class="ax_default text_field" data-label="Machine Name">         <input id="machine_name_out_out" type="text" placeholder="{{machine_name_out_out}}"/>       </div>        <!-- Time Period (Text Field) param time_period-->       <div id="u37" class="ax_default text_field" data-label="Time Period">         <input id="time_period_out" type="text" placeholder="{{time_period_out}}"/>       </div>        <!-- Data Points (Text Field) param data_points-->       <div id="u38" class="ax_default text_field" data-label="machine_status_out">         <input id="machine_status_out" type="text" placeholder="{{machine_status_out}}"/>       </div>        <!-- Ampere (Text Field) param current-->       <div id="u39" class="ax_default text_field" data-label="timestamp_status_update_out">         <input id="timestamp_status_update_out" type="text" placeholder="{{timestamp_status_update_out}}"/>       </div>        <!-- x (Text Field) param accx-->       <div id="u40" class="ax_default text_field" data-label="part_count_out">         <input id="part_count_out" type="text" placeholder="{{part_count_out}}"/>       </div>        <!-- y (Text Field) param accy-->       <div id="u41" class="ax_default text_field" data-label="machine_utilization_out">         <input id="machine_utilization_out" type="text" placeholder="{{machine_utilization_out}}"/>       </div>        <!-- z (Text Field) param accz-->       <div id="u42" class="ax_default text_field" data-label="oee_out">         <input id="oee_out" type="text" placeholder="{{oee_out}}"/>       </div>        <!-- comment (Text Field) param comment-->       <div id="u43" class="ax_default text_field" data-label="comment">         <input id="comment_out" type="text" value="{{comment_out}}"/>       </div>        <!-- Connection Status (Rectangle) -->       <div id="u44" class="ax_default box_1" data-label="Connection Status">         <div id="u44_div" class=""></div>         <!-- Unnamed () -->         <div id="u45" class="text">           <p><span>Connection Status:</span></p>         </div>       </div>        <!-- Machine Name (Rectangle) -->       <div id="u46" class="ax_default box_1" data-label="Machine Name">         <div id="u46_div" class=""></div>         <!-- Unnamed () -->         <div id="u47" class="text">           <p><span>Machine Name:</span></p>         </div>       </div>        <!-- Time Period (Rectangle) -->       <div id="u48" class="ax_default box_1" data-label="Time Period">         <div id="u48_div" class=""></div>         <!-- Unnamed () -->         <div id="u49" class="text">           <p><span>Time Period (hours):</span></p>         </div>       </div>        <!-- Data Points (Rectangle) -->       <div id="u50" class="ax_default box_1" data-label="Data Points">         <div id="u50_div" class=""></div>         <!-- Unnamed () -->         <div id="u51" class="text">           <p><span>Machine Status:</span></p>         </div>       </div>        <!-- Ampere (Rectangle) -->       <div id="u52" class="ax_default box_1" data-label="Ampere">         <div id="u52_div" class=""></div>         <!-- Unnamed () -->         <div id="u53" class="text">           <p><span>Last Status Update:</span></p>         </div>       </div>        <!-- x (Rectangle) -->       <div id="u54" class="ax_default box_1" data-label="x">         <div id="u54_div" class=""></div>         <!-- Unnamed () -->         <div id="u55" class="text">           <p><span>Part Count:</span></p>         </div>       </div>        <!-- y (Rectangle) -->       <div id="u56" class="ax_default box_1" data-label="y">         <div id="u56_div" class=""></div>         <!-- Unnamed () -->         <div id="u57" class="text">           <p><span>Machine Utilization (%):</span></p>         </div>       </div>        <!-- z (Rectangle) -->       <div id="u58" class="ax_default box_1" data-label="z">         <div id="u58_div" class=""></div>         <!-- Unnamed () -->         <div id="u59" class="text">           <p><span>OEE (%):</span></p>         </div>       </div>        <!-- Comment (Rectangle) -->       <div id="u60" class="ax_default box_1" data-label="Comment">         <div id="u60_div" class=""></div>         <!-- Unnamed () -->         <div id="u61" class="text">           <p><span>Comment:</span></p>         </div>       </div>             </div>   </body> </html>  """)
        f.write("\n")
        f.write("connection_out = Failure\n" )
        f.write("machine_name_out_out = NA\n" )
        f.write("machine_name_out = "+str(inputdict['machine_name_in'])+"\n" )
        f.write("time_period_out = NA\n")
        f.write("machine_status_out = NA\n")
        f.write("timestamp_status_update_out = NA\n")
        f.write("part_count_out = NA\n")
        f.write("machine_utilization_out = NA\n")
        f.write("oee_out = NA\n")
        f.write("location_out= NA\n")
        f.write("comment_out = ERROR: Is the server running on host 152.1.58.206 and port 5432? If yes, check the login credentials!\n")
        f.write("ipaddress_out = "+str(inputdict['ipaddress_in'])+"\n")
        f.write("port_out = "+str(inputdict['port_in'])+"\n")
        f.write("dbname_out = "+str(inputdict['dbname_in'])+"\n")
        f.write("username_out = "+str(inputdict['username_in'])+"\n")
        f.write("password_out = XXXXX\n")
        f.write("start_out = "+str(inputdict['start_in'])+"\n")
        f.write("end_out = "+str(inputdict['end_in'])+"\n")
        f.write("ret_full_dataset_out = 0.0\n")
        f.write("snap_view_out = 0.0\n")
