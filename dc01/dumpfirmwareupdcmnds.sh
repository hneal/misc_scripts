# generate list of commands per BAY/REB needed for firmware updates 
# the dsm_map.txt input come from the dsm_source_editor camera dump
#
# - Homer
# #########################################################
awk '/\//{split($1,aa,"/");c1="";c2="";c3="";
rfirm="REB_v5_top_31385006.bit"; wfirm="WREB_v4_11384004.bit" ; gfirm="GREB_v2_21382007.bit" ; \
split($3,bs,"/"); bay = bs[1]; slot = bs[2] ; \
if (bay=="0" || bay=="44" || bay == "4" || bay == "40") { if (slot == "0") {firm = wfirm} else {firm = gfirm} } else {firm = rfirm} ; \
if ($3!="N/D") c1="\n\nBAY/SLOT = "$3"\nssh root@`atca_ip ir2-camera/"aa[1]"/4/0 --ifname lsst-daq`\nminicom -w bay"aa[2]"."aa[3]"\nrrs_load -f /mnt/nfs/reb_firmware/"firm" -s 1 -p 0"; \
split($4,bs,"/"); bay = bs[1]; slot = bs[2] ; \
if (bay=="0" || bay=="44" || bay == "4" || bay == "40") { if (slot == "0") {firm = wfirm} else {firm = gfirm} } else {firm = rfirm} ; \
if ($4!="N/D") c2="\n\nBAY/SLOT = "$4"\nssh root@`atca_ip ir2-camera/"aa[1]"/4/0 --ifname lsst-daq`\nminicom -w bay"aa[2]"."aa[3]"\nrrs_load -f /mnt/nfs/reb_firmware/"firm" -s 1 -p 1"; \
split($5,bs,"/"); bay = bs[1]; slot = bs[2] ; \
if (bay=="0" || bay=="44" || bay == "4" || bay == "40") { if (slot == "0") {firm = wfirm} else {firm = gfirm} } else {firm = rfirm} ; \
if ($5!="N/D") c3="\n\nBAY/SLOT = "$5"\nssh root@`atca_ip ir2-camera/"aa[1]"/4/0 --ifname lsst-daq`\nminicom -w bay"aa[2]"."aa[3]"\nrrs_load -f /mnt/nfs/reb_firmware/"firm" -s 1 -p 2"; \
print "\n------------------- \n\n"$1,$3,$4,$5,c1,c2,c3}' dsm_map.txt | more
