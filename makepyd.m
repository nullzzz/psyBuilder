function makepyd(clearHisOnly)

if ~exist('clearHisOnly','var')
    clearHisOnly = false;
end


directory = fullfile(pwd,'ptbGui');
deleteFiles(directory,'*.pyd');
deleteFiles(directory,'*.c');

if ~clearHisOnly
    untouchedFiles = {fullfile(directory,'run.py'),fullfile(directory,'doNothing.py'),fullfile(directory,'app\center\events\slider\item\textItem.py')};
    
    touchedFiles = {fullfile(directory,'app\menubar\compile_PTB.py')};
    
    files= dirall(directory,'\*.py',[],{'__init__.py'});
    failedFileIdx = [];
    errorResults = {};
    iError = 1;
    for iFile = 1:numel(files)
        
                
        if ~ismember(files(iFile).name,untouchedFiles) && ismember(files(iFile).name,touchedFiles)
            
            [status,result] = system(['cythonize -i -3 ',files(iFile).name]);
            [cpath,cfilename,cSuffix] = fileparts(files(iFile).name);
            
            if status ~= 0
                failedFileIdx = [failedFileIdx,iFile];
                
                cprintf('err',    'failed compiling:%-15s | %s\n',[cfilename,cSuffix],cpath);
                printErrorInfo(result);
                errorResults{iError} = result;
                iError = iError +1;
            else
                [status,result] = system(['ren "',fullfile(cpath,[cfilename,'.cp38-win_amd64.pyd']),'" ',cfilename,'.pyd']);
            end
            [status,result] = system(['del /F/S/Q "',fullfile(cpath,[cfilename,'.c']),'"']);
        end
    end
    
    disp(files(failedFileIdx));
    
end


