function printErrorInfo(result)
a = regexp(result,char(10),'split');
borderStr = '------------------------------------------------------------';


borderNums = find(ismember(a,borderStr));

if rem(numel(borderNums),2) == 1
    borderNums(end) = [];
end 
 
borderNums = reshape(borderNums,2,numel(borderNums)/2);

allRows = [];

for iCol = 1:size(borderNums,2)
    allRows = [allRows,borderNums(1,iCol):borderNums(2,iCol)];
end


for iRow = 1:numel(allRows)
   fprintf('%s\n',a{allRows(iRow)}); 
end