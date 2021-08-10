-- some random script i pulled off of GameGuardian's website
-- credit goes to ZineaHUN i guess.

function Complier(A0_24)
end
gg.toast("By ZineaHUN")
gg.alert("Always seek the way that is fair to others. The opportunity itself is not a fraud. At that moment you cheat as soon as you are not fair to the other fair players.")
function START()
menu = gg.multiChoice({"Speedhack (slow) (Just backwards)ON","Speedhack (slow) (Just backwards)OFF","Speedhack  very fast speed Oo (Just backwards)ON","Speedhack  very fast speed Oo (Just backwards)OFF","Speedhack ON","Speedhack OFF","Server synchronization ON","Server synchronization OFF","Teleport","Maximum distance from character ON","Maximum distance from character OFF","Exit"},nil,"By ZineaHUN")
if menu == nil then
else
if menu[1] == true then
mn1()
end
if menu[2] == true then
mn2()
end
if menu[3] == true then
mn3()
end
if menu[4] == true then
mn4()
end
if menu[5] == true then
mn5()
end
if menu[6] == true then
mn6()
end
if menu[7] == true then
mn7()
end
if menu[8] == true then
mn8()
end
if menu[9] == true then
mn9()
end
if menu[10] == true then
mn10()
end
if menu[11] == true then
mn11()
end
if menu[12] == true then
exit()
end
end
AGYT = -1
end
function mn1()
gg.setRanges(gg.REGION_CODE_APP)
gg.toast('Starting Speedhack slow just backwards ON!')
gg.clearResults(950)
gg.searchNumber('0.4000000000596', gg.TYPE_FLOAT, false, gg.SIGN_EQUAL, 0, -1)
gg.searchNumber('0.4000000000596', gg.TYPE_FLOAT, false, gg.SIGN_EQUAL, 0, -1)
gg.getResults(950)
print('Replaced: ', gg.editAll('5', gg.TYPE_FLOAT))
gg.toast(' Speedhack slow just backwards ON, activated! ')
end
function mn2()
gg.setRanges(gg.REGION_CODE_APP)
gg.toast('Starting Speedhack slow just backwards OFF!')
gg.clearResults(950)
gg.searchNumber('5', gg.TYPE_FLOAT, false, gg.SIGN_EQUAL, 0, -1)
gg.searchNumber('5', gg.TYPE_FLOAT, false, gg.SIGN_EQUAL, 0, -1)
gg.getResults(950)
print('Replaced: ', gg.editAll('0.4000000000596', gg.TYPE_FLOAT))
gg.toast(' Speedhack slow just backwards OFF, activated ')

end
function mn3()
gg.setRanges(gg.REGION_CODE_APP)
gg.toast('Starting Speedhack very fast, just backwards ON')
gg.clearResults(950)
gg.searchNumber('0.4000000000596', gg.TYPE_FLOAT, false, gg.SIGN_EQUAL, 0, -1)
gg.searchNumber('0.4000000000596', gg.TYPE_FLOAT, false, gg.SIGN_EQUAL, 0, -1)
gg.getResults(950)
print('Replaced: ', gg.editAll('30', gg.TYPE_FLOAT))
gg.toast(' Speedhack very fast, just backwards ON, activated! ')
end
function mn4()
gg.setRanges(gg.REGION_CODE_APP)
gg.toast('Starting Speedhack very fast, just backwards OFF')
gg.clearResults(950)
gg.searchNumber('30', gg.TYPE_FLOAT, false, gg.SIGN_EQUAL, 0, -1)
gg.searchNumber('30', gg.TYPE_FLOAT, false, gg.SIGN_EQUAL, 0, -1)
gg.getResults(950)
print('Replaced: ', gg.editAll('0.4000000000596', gg.TYPE_FLOAT))
gg.toast(' Speedhack very fast, just backwards OFF, activated! ')
end
function mn5()
gg.setRanges(gg.REGION_CODE_APP)
gg.toast('Starting Speedhack ON!')
gg.clearResults(14)
gg.searchNumber("0.001;180;-180::25", gg.TYPE_FLOAT, false, gg.SIGN_EQUAL, 0, -1)
gg.searchNumber("0.001", gg.TYPE_FLOAT, false, gg.SIGN_EQUAL, 0, -1)
gg.getResults(14)
print('Replaced: ', gg.editAll("0.003", gg.TYPE_FLOAT))
gg.toast(' Speedhack ON, activated! ')
end
function mn6()
gg.setRanges(gg.REGION_CODE_APP)
gg.toast('Starting Speedhack OFF!')
gg.clearResults(1)
gg.searchNumber("0.003;360;-360::25", gg.TYPE_FLOAT, false, gg.SIGN_EQUAL, 0, -1)
gg.searchNumber("0.003", gg.TYPE_FLOAT, false, gg.SIGN_EQUAL, 0, -1)
gg.getResults(1)
print('Replaced: ', gg.editAll("0.001", gg.TYPE_FLOAT))
gg.toast(' Speedhack OFF, activated! ')
end
function mn7()
gg.setRanges(gg.REGION_C_DATA)
gg.toast('Starting Sync (forward) ON')
gg.clearResults(900)
gg.searchNumber('1148846080', gg.TYPE_DWORD, false, gg.SIGN_EQUAL, 0, -1)
gg.searchNumber('1148846080', gg.TYPE_DWORD, false, gg.SIGN_EQUAL, 0, -1)
gg.getResults(900)
print(' Replaced: ', gg.editAll('-10', gg.TYPE_DWORD))
gg.toast(' Starting Sync (foward) ON ' )
end
function mn8()
    gg.setRanges(gg.REGION_C_DATA)
gg.toast('Starting Sync OFF')
gg.clearResults(900)
gg.searchNumber('-10', gg.TYPE_DWORD, false, gg.SIGN_EQUAL, 0, -1)
gg.searchNumber('-10', gg.TYPE_DWORD, false, gg.SIGN_EQUAL, 0, -1)
gg.getResults(900)
print(' Replaced: ', gg.editAll('1148846080', gg.TYPE_DWORD))
gg.toast(' Starting Sync OFF ')
end
function mn9()
gg.setRanges(gg.REGION_C_ALLOC)
gg.clearResults()
gg.searchNumber("522;-1;2;-1;-1;1,065,353,216;0~~522;0~~522;0~~522;-1::373",gg.TYPE_DWORD,false,gg.SIGN_EQUAL,0, -1)
gg.refineNumber("1065353216;0~~522;0~~522;0~~522;-1::273", gg.TYPE_DWORD, false, gg.SIGN_EQUAL, 0, -1)
gg.refineNumber("0~~522;0~~522;0~~522;-1::165", gg.TYPE_DWORD, false, gg.SIGN_EQUAL, 0, -1)
revert = gg.getResults(3, nil, nil, nil, nil, nil, nil, nil, nil)
local t = gg.getResults(3, nil, nil, nil, nil, nil, nil, nil, nil)
gg.addListItems(t)
t=nil

OO()
end

function OO()
XO1=1
XOX1=-1
menu1 = gg.choice({
'Teleport coordinates1',
'Teleport coordinates2',
'Teleport coordinates3',
'Teleport coordinates4',
'Teleport coordinates5',
'Teleport coordinates6',
'Teleport coordinates7',
'Teleport coordinates8',
'Teleport coordinates9',
'Teleport coordinates10',
'Teleport coordinates11',
'Teleport coordinates12',
'Teleport coordinates13',
'Clear the record and take the point again！',
'go back to the last page'},
nil,'Go to the coordinate point that needs to be recorded and select a coordinate point.  The first click is to take the point, and then click to teleport the position directly!')
if menu1 == 1 then oo1() end
if menu1 == 2 then oo2() end
if menu1 == 3 then oo3() end
if menu1 == 4 then oo4() end
if menu1 == 5 then oo5() end
if menu1 == 6 then oo6() end
if menu1 == 7 then oo7() end
if menu1 == 8 then oo8() end
if menu1 == 9 then oo9() end
if menu1 == 10 then oo10() end
if menu1 == 11 then oo11() end
if menu1 == 12 then oo12() end
if menu1 == 13 then oo13() end
if menu1 == 14 then oo14() end
if menu1 == 15 then XO1=nil HOME() end

 if XO1 == 1 then
  while(true)do
    if gg.isVisible(true) then
XOX1=1
gg.setVisible(false)
     end
     if XOX1==1 then
OO()
     end
   end
 end

end


function oo1()
if revert1 == nil then 
   revert1 = gg.getResults(3, nil, nil, nil, nil, nil, nil, nil, nil)
   gg.toast("Take the point successfully, click again to teleport this position directly！")
   end

   if revert1 ~= nil then gg.setValues(revert1) 
   gg.toast("Teleport success！")
   end
end

function oo2()
   if revert2 == nil then 
   revert2 = gg.getResults(3, nil, nil, nil, nil, nil, nil, nil, nil)
   gg.toast("Take the point successfully, click again to teleport this position directly！")
   end

   if revert2 ~= nil then gg.setValues(revert2) 
   gg.toast("Teleport success！")
   end
end

function oo3()
   if revert3 == nil then 
   revert3 = gg.getResults(3, nil, nil, nil, nil, nil, nil, nil, nil)
   gg.toast("Take the point successfully, click again to teleport this position directly！")
   end

   if revert3 ~= nil then gg.setValues(revert3) 
   gg.toast("Teleport success！")
   end
end

function oo4()
   if revert4 == nil then 
   revert4 = gg.getResults(3, nil, nil, nil, nil, nil, nil, nil, nil)
   gg.toast("Take the point successfully, click again to teleport this position directly！")
   end

   if revert4 ~= nil then gg.setValues(revert4) 
   gg.toast("Teleport success！")
   end
end

function oo5()
   if revert5 == nil then 
   revert5 = gg.getResults(3, nil, nil, nil, nil, nil, nil, nil, nil)
   gg.toast("Take the point successfully, click again to teleport this position directly！")
   end

   if revert5 ~= nil then gg.setValues(revert5) 
   gg.toast("Teleport success！")
   end
end

function oo6()
   if revert6 == nil then 
   revert6 = gg.getResults(3, nil, nil, nil, nil, nil, nil, nil, nil)
   gg.toast("Take the point successfully, click again to teleport this position directly！")
   end

   if revert6 ~= nil then gg.setValues(revert6) 
   gg.toast("Teleport success！")
   end
end

function oo7()
   if revert7 == nil then 
   revert7 = gg.getResults(3, nil, nil, nil, nil, nil, nil, nil, nil)
   gg.toast("Take the point successfully, click again to teleport this position directly！")
   end

   if revert7 ~= nil then gg.setValues(revert7) 
   gg.toast("Teleport success！")
   end
end

function oo8()
   if revert8 == nil then 
   revert8 = gg.getResults(3, nil, nil, nil, nil, nil, nil, nil, nil)
   gg.toast("Take the point successfully, click again to teleport this position directly！")
   end

   if revert8 ~= nil then gg.setValues(revert8) 
   gg.toast("Teleport success！")
   end
end



function oo9()
   if revert9 == nil then 
   revert9 = gg.getResults(3, nil, nil, nil, nil, nil, nil, nil, nil)
   gg.toast("Take the point successfully, click again to teleport this position directly！")
   end

   if revert9 ~= nil then gg.setValues(revert9) 
   gg.toast("Teleport success！")
   end
end

function oo10()
   if revert10 == nil then 
   revert10 = gg.getResults(3, nil, nil, nil, nil, nil, nil, nil, nil)
   gg.toast("Take the point successfully, click again to teleport this position directly！")
   end

   if revert10 ~= nil then gg.setValues(revert10) 
   gg.toast("Teleport success！")
   end
end

function oo11()
   if revert11 == nil then 
   revert11 = gg.getResults(3, nil, nil, nil, nil, nil, nil, nil, nil)
   gg.toast("Take the point successfully, click again to teleport this position directly！")
   end

   if revert11 ~= nil then gg.setValues(revert11) 
   gg.toast("Teleport success！")
   end
end

function oo12()
   if revert12 == nil then 
   revert12 = gg.getResults(3, nil, nil, nil, nil, nil, nil, nil, nil)
   gg.toast("Take the point successfully, click again to teleport this position directly！")
   end

   if revert12 ~= nil then gg.setValues(revert12) 
   gg.toast("Teleport success！")
   end
end

function oo13()
   if revert13 == nil then 
   revert13 = gg.getResults(3, nil, nil, nil, nil, nil, nil, nil, nil)
   gg.toast("Take the point successfully, click again to teleport this position directly！")
   end

   if revert13 ~= nil then gg.setValues(revert12) 
   gg.toast("Teleport success！")
   end
end


function oo14()
revert1 = nil
revert2 = nil
revert3 = nil
revert4 = nil
revert5 = nil
revert6 = nil
revert7 = nil
revert8 = nil
gg.toast("The coordinate record is cleared!  Please take another point！")



end

function mn10()
gg.setRanges(gg.REGION_CODE_APP)
gg.toast('Starting maxdistance ON !')
gg.clearResults(850)
gg.searchNumber('9', gg.TYPE_DWORD, false, gg.SIGN_EQUAL, 0, -1)
gg.searchNumber('9', gg.TYPE_DWORD, false, gg.SIGN_EQUAL, 0, -1)
gg.getResults(850)
print('Replaced: ', gg.editAll('19164', gg.TYPE_DWORD))
gg.toast('Maxdistance ON, activated! ')
end

function mn11()
gg.setRanges(gg.REGION_CODE_APP)
gg.toast('Starting maxdistance OFF!')
gg.clearResults(850)
gg.searchNumber('19164', gg.TYPE_DWORD, false, gg.SIGN_EQUAL, 0, -1)
gg.searchNumber('19164', gg.TYPE_DWORD, false, gg.SIGN_EQUAL, 0, -1)
gg.getResults(850)
print('Replaced: ', gg.editAll('9', gg.TYPE_DWORD))
gg.toast('Maxdistance OFF, activated! ')
end

function HOME()
gg.setRanges(gg.REGION_C_ALLOC | gg.REGION_CODE_APP)
gg.toast("HOME")
print('HOME')
START()
end

function exit()
gg.alert("Thanks to everyone for helping, without whom this script could not have been created!  Special thanks to the creator of the Hackers house youtube channel!  Good game for everyone!  ZineaHUN")
gg.copyText("https://m.youtube.com/channel/UC4FquNZKdBgMY1sCNBqg_gA")
os.exit()
end
while true do
if gg.isVisible(true) then
AGYT = 1
gg.setVisible(false)
end
if AGYT == 1 then
START()
end
end