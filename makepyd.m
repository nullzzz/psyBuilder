function makepyd(clearHisOnly,runAllMatchFiles)

if ~exist('clearHisOnly','var')
    clearHisOnly = false;
end


if ~exist('runAllMatchFiles','var')
    runAllMatchFiles = true;
end


directory = fileparts(mfilename('fullpath'));
deleteFiles(directory,'*.pyd');
deleteFiles(directory,'*.c');

if ~clearHisOnly
    untouchedFiles = {mkFullFile(directory,'run.py'),mkFullFile(directory,'doNothing.py'),mkFullFile(directory,'app\center\events\slider\item\textItem.py')};
    
    touchedFiles = {mkFullFile(directory,'app\menubar\compile_PTB.py')};
    
    files= dirall(directory,'*.py',[],{'__init__.py'});
    failedFileIdx = [];
    errorResults = {};
    iError = 1;
    for iFile = 1:numel(files)
        
        
        if ~ismember(files(iFile).name,untouchedFiles) && (runAllMatchFiles||ismember(files(iFile).name,touchedFiles))
            
            [status,result] = system(['cythonize -i -3 ',files(iFile).name]);
            [cpath,cfilename,cSuffix] = fileparts(files(iFile).name);
            
            if status ~= 0
                failedFileIdx = [failedFileIdx,iFile];
                
                cprintf('err',    'failed compiling:%-15s | %s\n',[cfilename,cSuffix],cpath);
                printErrorInfo(result);
                errorResults{iError} = result;
                iError = iError +1;
            else
                if IsWin
                    [status,result] = system(['ren "',fullfile(cpath,[cfilename,'.cp38-win_amd64.pyd']),'" ',cfilename,'.pyd']);
                end
            end
            if IsWin
                [status,result] = system(['del /F/S/Q "',fullfile(cpath,[cfilename,'.c']),'"']);
            else
                [status,result] = system(['rm -rf "',fullfile(cpath,[cfilename,'.c']),'"']);
            end
        end
    end
    
    disp(files(failedFileIdx));
    
end

end

function fullFileName = mkFullFile(directory,filename)

temp = regexp(filename,'[\\/]','split');
fullFileName = fullfile(directory,temp{:});
end


