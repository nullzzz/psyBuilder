function varargout = subjectInfo(varargin)
% SUBJECTINFO M-file for subjectInfo.fig
%      SUBJECTINFO, by itself, creates a new SUBJECTINFO or raises the existing
%      singleton*.
%
%      H = SUBJECTINFO returns the handle to a new SUBJECTINFO or the handle to
%      the existing singleton*.
%
%      SUBJECTINFO('CALLBACK',hObject,eventData,handles,...) calls the local
%      function named CALLBACK in SUBJECTINFO.M with the given input arguments.
%
%      SUBJECTINFO('Property','Value',...) creates a new SUBJECTINFO or raises the
%      existing singleton*.  Starting from the left, property value pairs are
%      applied to the GUI before subjectinfo_OpeningFunction gets called.  An
%      unrecognized property name or invalid value makes property application
%      stop.  All inputs are passed to subjectInfo_OpeningFcn via varargin.
%
%      *See GUI Options on GUIDE's Tools menu.  Choose "GUI allows only one
%      instance to run (singleton)".
%
% See also: GUIDE, GUIDATA, GUIHANDLES

% Edit the above text to modify the response to help subjectInfo

% Last Modified by GUIDE v2.5 08-Jun-2020 13:06:53

% Begin initialization code - DO NOT EDIT
gui_Singleton = 1;
gui_State = struct('gui_Name',       mfilename, ...
                   'gui_Singleton',  gui_Singleton, ...
                   'gui_OpeningFcn', @subjectInfo_OpeningFcn, ...
                   'gui_OutputFcn',  @subjectInfo_OutputFcn, ...
                   'gui_LayoutFcn',  @subjectInfo_LayoutFcn, ...
                   'gui_Callback',   []);
if nargin && ischar(varargin{1})
    gui_State.gui_Callback = str2func(varargin{1});
end

if nargout
    [varargout{1:nargout}] = gui_mainfcn(gui_State, varargin{:});
else
    gui_mainfcn(gui_State, varargin{:});
end
% End initialization code - DO NOT EDIT


% --- Executes just before subjectInfo is made visible.
function subjectInfo_OpeningFcn(hObject, eventdata, handles, varargin)
% This function has no output args, see OutputFcn.
% hObject    handle to figure
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)
% varargin   command line arguments to subjectInfo (see VARARGIN)

% Choose default command line output for subjectInfo
handles.output = hObject;

if numel(varargin) > 1
	sessionDefault = varargin{2};
    
    if ~ischar(sessionDefault)
        sessionDefault = num2str(sessionDefault);
    end
else
    sessionDefault = [];
end

if ~isempty(sessionDefault)
    set(handles.session,'String',sessionDefault);	
end 

if numel(varargin) > 0
    expNameStr = varargin{1};
else
    error('subjectinfo require at least one input parameter!');
end 

handles.expName = expNameStr;

savePath = fileparts(mfilename('fullpath'));

try %#ok<TRYNC>
	lastSavedData = load(fullfile(savePath,'last.subinfo'),'-mat');

	set(handles.name,'String',lastSavedData.output.name);	
	set(handles.age,'String',lastSavedData.output.age);	
	
	if strcmpi(lastSavedData.output.gender,'female')
		set(handles.gender,'Value',2);
	end	

	% set(handles.gender,'String',lastSavedData.output.gender);	
	
	if strcmpi(lastSavedData.output.hand,'right_hand')
		set(handles.hand,'Value',2);
	end

	% set(handles.hand,'String',lastSavedData.output.hand);
		
	set(handles.num,'String',num2str(str2double(lastSavedData.output.num)+1));	
    
    if isempty(sessionDefault)
        sessionDefault = lastSavedData.output.session;	
    end


    set(handles.session,'String',sessionDefault);	

    clear lastSavedData;

end

handles.isQuit = 0;
% Update handles structure
guidata(hObject, handles);

% UIWAIT makes subjectInfo wait for user response (see UIRESUME)
 uiwait(handles.figure1);


% --- Outputs from this function are returned to the command line.
function varargout = subjectInfo_OutputFcn(hObject, eventdata, handles) 
% varargout  cell array for returning output args (see VARARGOUT);
% hObject    handle to figure
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)

% Get default command line output from handles structure
if isempty(handles)
    varargout{1}=[];
else
    output.name = get(handles.name,'String');
    output.age = get(handles.age,'String');
    
    if get(handles.gender,'Value')==1
        output.gender='male';
    else
        output.gender='female';
    end
    % output.gender = get(handles.gender,'Value');
    if get(handles.hand,'Value')==1
        output.hand ='left_hand';
    else
        output.hand ='right_hand';
    end
    
    output.num      = get(handles.num,'String');
    output.session  = get(handles.session,'String');
    output.filename = [handles.expName,'_',output.num,'_',output.session];
    
    
    % guidata(hObject,handles);
    delete(handles.figure1);
    %-- save last subinfo--/
    savePath = fileparts(mfilename('fullpath'));
    %----------------------\
    
    
    if handles.isQuit
        varargout{1}=[];
    else
        varargout{1}=output;
        save(fullfile(savePath,'last.subinfo'),'output');
    end


end



function name_Callback(hObject, eventdata, handles)
% hObject    handle to name (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)

% Hints: get(hObject,'String') returns contents of name as text
%        str2double(get(hObject,'String')) returns contents of name as a double
guidata(hObject,handles);

% --- Executes during object creation, after setting all properties.
function name_CreateFcn(hObject, eventdata, handles)
% hObject    handle to name (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    empty - handles not created until after all CreateFcns called

% Hint: edit controls usually have a white background on Windows.
%       See ISPC and COMPUTER.
if ispc && isequal(get(hObject,'BackgroundColor'), get(0,'defaultUicontrolBackgroundColor'))
    set(hObject,'BackgroundColor','white');
end


% --- Executes on button press in gender.
function gender_Callback(hObject, eventdata, handles)
% hObject    handle to gender (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)

% Hint: get(hObject,'Value') returns toggle state of gender
guidata(hObject,handles);


function age_Callback(hObject, eventdata, handles)
% hObject    handle to age (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)

% Hints: get(hObject,'String') returns contents of age as text
%        str2double(get(hObject,'String')) returns contents of age as a double
guidata(hObject,handles);

% --- Executes during object creation, after setting all properties.
function age_CreateFcn(hObject, eventdata, handles)
% hObject    handle to age (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    empty - handles not created until after all CreateFcns called

% Hint: edit controls usually have a white background on Windows.
%       See ISPC and COMPUTER.
if ispc && isequal(get(hObject,'BackgroundColor'), get(0,'defaultUicontrolBackgroundColor'))
    set(hObject,'BackgroundColor','white');
end


% --- Executes on button press in hand.
function hand_Callback(hObject, eventdata, handles)
% hObject    handle to hand (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)

% Hint: get(hObject,'Value') returns toggle state of hand
guidata(hObject,handles);

% --- Executes on button press in sub_yes.
function sub_yes_Callback(hObject, eventdata, handles)
% hObject    handle to sub_yes (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)
savePath = fileparts(mfilename('fullpath'));

outputFilename = [handles.expName,'_',get(handles.num,'String'),'_',get(handles.session,'String'),'.mat'];

if exist(fullfile(savePath,outputFilename),'file')
    set(handles.figure1,'Visible','off');
    isOverWrite = OverwriteOrNot(outputFilename);
    
    if isOverWrite
        uiresume;
    else
        set(handles.figure1,'Visible','on');
    end 
else
    uiresume;
end
guidata(hObject,handles);





% --- Executes on button press in sub_final.
function sub_final_Callback(hObject, eventdata, handles)
% hObject    handle to sub_final (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)
handles.isQuit = 1;
guidata(hObject,handles);
uiresume;
% delete(handles.figure1);



% --- Executes on selection change in popupmenu1.
function popupmenu1_Callback(hObject, eventdata, handles)
% hObject    handle to popupmenu1 (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)

% Hints: contents = get(hObject,'String') returns popupmenu1 contents as cell array
%        contents{get(hObject,'Value')} returns selected item from popupmenu1


% --- Executes during object creation, after setting all properties.
function popupmenu1_CreateFcn(hObject, eventdata, handles)
% hObject    handle to popupmenu1 (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    empty - handles not created until after all CreateFcns called

% Hint: popupmenu controls usually have a white background on Windows.
%       See ISPC and COMPUTER.
if ispc && isequal(get(hObject,'BackgroundColor'), get(0,'defaultUicontrolBackgroundColor'))
    set(hObject,'BackgroundColor','white');
end



function num_Callback(hObject, eventdata, handles)
% hObject    handle to num (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)

% Hints: get(hObject,'String') returns contents of num as text
%        str2double(get(hObject,'String')) returns contents of num as a double
guidata(hObject,handles);

% --- Executes during object creation, after setting all properties.
function num_CreateFcn(hObject, eventdata, handles)
% hObject    handle to num (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    empty - handles not created until after all CreateFcns called

% Hint: edit controls usually have a white background on Windows.
%       See ISPC and COMPUTER.
if ispc && isequal(get(hObject,'BackgroundColor'), get(0,'defaultUicontrolBackgroundColor'))
    set(hObject,'BackgroundColor','white');
end



function session_Callback(hObject, eventdata, handles)
% hObject    handle to session (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)

% Hints: get(hObject,'String') returns contents of session as text
%        str2double(get(hObject,'String')) returns contents of session as a double
guidata(hObject,handles);

% --- Executes during object creation, after setting all properties.
function session_CreateFcn(hObject, eventdata, handles)
% hObject    handle to session (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    empty - handles not created until after all CreateFcns called

% Hint: edit controls usually have a white background on Windows.
%       See ISPC and COMPUTER.
if ispc && isequal(get(hObject,'BackgroundColor'), get(0,'defaultUicontrolBackgroundColor'))
    set(hObject,'BackgroundColor','white');
end




% --- Executes during object creation, after setting all properties.
function gender_CreateFcn(hObject, eventdata, handles)
% hObject    handle to gender (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    empty - handles not created until after all CreateFcns called

% Hint: listbox controls usually have a white background on Windows.
%       See ISPC and COMPUTER.
if ispc && isequal(get(hObject,'BackgroundColor'), get(0,'defaultUicontrolBackgroundColor'))
    set(hObject,'BackgroundColor','white');
end


% --- Executes during object creation, after setting all properties.
function hand_CreateFcn(hObject, eventdata, handles)
% hObject    handle to hand (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    empty - handles not created until after all CreateFcns called

% Hint: popupmenu controls usually have a white background on Windows.
%       See ISPC and COMPUTER.
if ispc && isequal(get(hObject,'BackgroundColor'), get(0,'defaultUicontrolBackgroundColor'))
    set(hObject,'BackgroundColor','white');
end




% --- Executes on key press with focus on sub_yes and none of its controls.
function sub_yes_KeyPressFcn(hObject, eventdata, handles)
% hObject    handle to sub_yes (see GCBO)
% eventdata  structure with the following fields (see MATLAB.UI.CONTROL.UICONTROL)
%	Key: name of the key that was pressed, in lower case
%	Character: character interpretation of the key(s) that was pressed
%	Modifier: name(s) of the modifier key(s) (i.e., control, shift) pressed
% handles    structure with handles and user data (see GUIDATA)
savePath = fileparts(mfilename('fullpath'));

outputFilename = [handles.expName,'_',get(handles.num,'String'),'_',get(handles.session,'String'),'.mat'];

guidata(hObject,handles);
if exist(fullfile(savePath,outputFilename),'file')
    set(handles.figure1,'Visible','off');
    isOverWrite = OverwriteOrNot(outputFilename);
    
    if isOverWrite
        uiresume;
    else
        set(handles.figure1,'Visible','on');
    end 
else
    uiresume;
end


% --- If Enable == 'on', executes on mouse press in 5 pixel border.
% --- Otherwise, executes on mouse press in 5 pixel border or over hand.
function hand_ButtonDownFcn(hObject, eventdata, handles)
% hObject    handle to hand (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)




% --- If Enable == 'on', executes on mouse press in 5 pixel border.
% --- Otherwise, executes on mouse press in 5 pixel border or over sub_yes.
function sub_yes_ButtonDownFcn(hObject, eventdata, handles)
% hObject    handle to sub_yes (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)

savePath = fileparts(mfilename('fullpath'));

outputFilename = [handles.expName,'_',get(handles.num,'String'),'_',get(handles.session,'String'),'.mat'];
guidata(hObject,handles);
if exist(fullfile(savePath,outputFilename),'file')
    set(handles.figure1,'Visible','off');
    isOverWrite = OverwriteOrNot(outputFilename);
    
    if isOverWrite
        uiresume;
    else
        set(handles.figure1,'Visible','on');
    end 
else
    uiresume;
end



% --- Executes during object creation, after setting all properties.
function sub_yes_CreateFcn(hObject, eventdata, handles)
% hObject    handle to sub_yes (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    empty - handles not created until after all CreateFcns called


% --- If Enable == 'on', executes on mouse press in 5 pixel border.
% --- Otherwise, executes on mouse press in 5 pixel border or over sub_final.
function sub_final_ButtonDownFcn(hObject, eventdata, handles)
% hObject    handle to sub_final (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)
handles.isQuit = 1;
guidata(hObject,handles);
uiresume;



% --- Executes on key press with focus on sub_final and none of its controls.
function sub_final_KeyPressFcn(hObject, eventdata, handles)
% hObject    handle to sub_final (see GCBO)
% eventdata  structure with the following fields (see MATLAB.UI.CONTROL.UICONTROL)
%	Key: name of the key that was pressed, in lower case
%	Character: character interpretation of the key(s) that was pressed
%	Modifier: name(s) of the modifier key(s) (i.e., control, shift) pressed
% handles    structure with handles and user data (see GUIDATA)
handles.isQuit = 1;
guidata(hObject,handles);
uiresume;

% --- Executes during object deletion, before destroying properties.
function sub_yes_DeleteFcn(hObject, eventdata, handles)
% hObject    handle to sub_yes (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)


% --- Creates and returns a handle to the GUI figure. 
function h1 = subjectInfo_LayoutFcn(policy)
% policy - create a new figure or use a singleton. 'new' or 'reuse'.

persistent hsingleton;
if strcmpi(policy, 'reuse') & ishandle(hsingleton)
    h1 = hsingleton;
    return;
end

bkColor = get(0,'defaultfigureColor');
appdata = [];
appdata.GUIDEOptions = struct(...
    'active_h', [], ...
    'taginfo', struct(...
    'figure', [], ...
    'uipanel', [], ...
    'text', 8, ...
    'edit', 6, ...
    'radiobutton', [], ...
    'checkbox', [], ...
    'togglebutton', [], ...
    'pushbutton', [], ...
    'slider', [], ...
    'popupmenu', [], ...
    'listbox', [], ...
    'uibuttongroup', []), ...
    'override', [], ...
    'release', 13, ...
    'resize', 'simple', ...
    'accessibility', 'callback', ...
    'mfile', [], ...
    'callbacks', [], ...
    'singleton', [], ...
    'syscolorfig', [], ...
    'blocking', 0, ...
    'lastSavedFile', 'D:\Yang\BCLtoolboxs1.0\psychtool\exp_nenu\ExpNenu GUI\export\subjectInfo.m', ...
    'lastFilename', 'D:\Yang\BCLtoolboxs1.0\psychtool\exp_nenu\ExpNenu GUI\subjectinfo.fig');
appdata.lastValidTag = 'figure1';
appdata.UsedByGUIData_m = [];
appdata.GUIDELayoutEditor = [];
appdata.initTags = struct(...
    'handle', [], ...
    'tag', 'figure1');

ttemp=get(0,'ScreenSize');
ScreenS = [(ttemp(3)-376)/2,(ttemp(4)-325)/2,376,325];

h1 = figure(...
'PaperUnits',get(0,'defaultfigurePaperUnits'),...
'Units',get(0,'defaultfigureUnits'),...
'Position',ScreenS,...
'Visible','on',...
'Color',get(0,'defaultfigureColor'),...
'IntegerHandle','off',...
'Colormap',[0 0 0.5625;0 0 0.625;0 0 0.6875;0 0 0.75;0 0 0.8125;0 0 0.875;0 0 0.9375;0 0 1;0 0.0625 1;0 0.125 1;0 0.1875 1;0 0.25 1;0 0.3125 1;0 0.375 1;0 0.4375 1;0 0.5 1;0 0.5625 1;0 0.625 1;0 0.6875 1;0 0.75 1;0 0.8125 1;0 0.875 1;0 0.9375 1;0 1 1;0.0625 1 1;0.125 1 0.9375;0.1875 1 0.875;0.25 1 0.8125;0.3125 1 0.75;0.375 1 0.6875;0.4375 1 0.625;0.5 1 0.5625;0.5625 1 0.5;0.625 1 0.4375;0.6875 1 0.375;0.75 1 0.3125;0.8125 1 0.25;0.875 1 0.1875;0.9375 1 0.125;1 1 0.0625;1 1 0;1 0.9375 0;1 0.875 0;1 0.8125 0;1 0.75 0;1 0.6875 0;1 0.625 0;1 0.5625 0;1 0.5 0;1 0.4375 0;1 0.375 0;1 0.3125 0;1 0.25 0;1 0.1875 0;1 0.125 0;1 0.0625 0;1 0 0;0.9375 0 0;0.875 0 0;0.8125 0 0;0.75 0 0;0.6875 0 0;0.625 0 0;0.5625 0 0],...
'MenuBar','none',...
'Name','subjectinfo',...
'NumberTitle','off',...
'Tag','figure1',...
'UserData',[],...
'PaperPosition',get(0,'defaultfigurePaperPosition'),...
'PaperSize',[20.99999864 29.69999902],...
'PaperType',get(0,'defaultfigurePaperType'),...
'InvertHardcopy',get(0,'defaultfigureInvertHardcopy'),...
'ScreenPixelsPerInchMode','manual',...
'HandleVisibility','callback',...
'CreateFcn', {@local_CreateFcn, blanks(0), appdata} ); 
set(h1,'WindowStyle','modal');

appdata = [];
appdata.lastValidTag = 'uipanel1';

h2 = uipanel(...
'Parent',h1,...
'FontUnits',get(0,'defaultuipanelFontUnits'),...
'Units',get(0,'defaultuipanelUnits'),...
'HighlightColor',[0 0 0],...
'ShadowColor',[1 1 1],...
'TitlePosition','centertop',...
'Title','Subject Information',...
'BackgroundColor',bkColor,...
'Tag','uipanel1',...
'Clipping','off',...
'Position',[-0.00265957446808511 -0.00615384615384615 1.00265957446809 1.00307692307692],...
'FontSize',12,...
'FontName','Arial',...
'CreateFcn', {@local_CreateFcn, blanks(0), appdata} );

appdata = [];
appdata.lastValidTag = 'text1';

h3 = uicontrol(...
'Parent',h2,...
'FontUnits',get(0,'defaultuicontrolFontUnits'),...
'Units','normalized',...
'String','Name:',...
'Style','text',...
'Position',[0.265415549597855 0.857142857142857 0.131367292225201 0.0714285714285714],...
'BackgroundColor',bkColor,...
'Children',[],...
'Tag','text1',...
'FontSize',12,...
'FontName','Arial',...
'CreateFcn', {@local_CreateFcn, blanks(0), appdata} );

appdata = [];
appdata.lastValidTag = 'text2';

h4 = uicontrol(...
'Parent',h2,...
'FontUnits',get(0,'defaultuicontrolFontUnits'),...
'Units','normalized',...
'String','Gender:',...
'Style','text',...
'Position',[0.2171581769437 0.574675324675325 0.179624664879357 0.0714285714285714],...
'BackgroundColor',bkColor,...
'Children',[],...
'Tag','text2',...
'FontSize',12,...
'FontName','Arial',...
'CreateFcn', {@local_CreateFcn, blanks(0), appdata} );

appdata = [];
appdata.lastValidTag = 'text3';

h5 = uicontrol(...
'Parent',h2,...
'FontUnits',get(0,'defaultuicontrolFontUnits'),...
'Units','normalized',...
'String','Age:',...
'Style','text',...
'Position',[0.289544235924933 0.724025974025974 0.107238605898123 0.0714285714285714],...
'BackgroundColor',bkColor,...
'Children',[],...
'Tag','text3',...
'FontSize',12,...
'FontName','Arial',...
'CreateFcn', {@local_CreateFcn, blanks(0), appdata} );

appdata = [];
appdata.lastValidTag = 'text4';

h6 = uicontrol(...
'Parent',h2,...
'FontUnits',get(0,'defaultuicontrolFontUnits'),...
'Units','normalized',...
'String','Handless:',...
'Style','text',...
'Position',[0.193029490616622 0.428571428571429 0.203753351206434 0.0779220779220779],...
'BackgroundColor',bkColor,...
'Children',[],...
'Tag','text4',...
'FontSize',12,...
'FontName','Arial',...
'CreateFcn', {@local_CreateFcn, blanks(0), appdata} );

appdata = [];
appdata.lastValidTag = 'sub_yes';

h7 = uicontrol(...
'Parent',h2,...
'FontUnits',get(0,'defaultuicontrolFontUnits'),...
'Units','normalized',...
'String','Ok',...
'Position',[0.168900804289544 0.100945471466644 0.227882037533512 0.095],...
'BackgroundColor',bkColor,...
'Callback',@(hObject,eventdata)subjectInfo('sub_yes_Callback',hObject,eventdata,guidata(hObject)),...
'Children',[],...
'ButtonDownFcn',@(hObject,eventdata)subjectInfo('sub_yes_ButtonDownFcn',hObject,eventdata,guidata(hObject)),...
'CreateFcn', {@local_CreateFcn, @(hObject,eventdata)subjectInfo('sub_yes_CreateFcn',hObject,eventdata,guidata(hObject)), appdata} ,...
'DeleteFcn',@(hObject,eventdata)subjectInfo('sub_yes_DeleteFcn',hObject,eventdata,guidata(hObject)),...
'Tag','sub_yes',...
'KeyPressFcn',@(hObject,eventdata)subjectInfo('sub_yes_KeyPressFcn',hObject,eventdata,guidata(hObject)),...
'FontSize',12,...
'FontName','Arial');

appdata = [];
appdata.lastValidTag = 'sub_final';

h8 = uicontrol(...
'Parent',h2,...
'FontUnits',get(0,'defaultuicontrolFontUnits'),...
'Units','normalized',...
'String','Quit',...
'Position',[0.571045576407507 0.100945471466644 0.227882037533512 0.095],...
'BackgroundColor',bkColor,...
'Callback',@(hObject,eventdata)subjectInfo('sub_final_Callback',hObject,eventdata,guidata(hObject)),...
'Children',[],...
'ButtonDownFcn',@(hObject,eventdata)subjectInfo('sub_final_ButtonDownFcn',hObject,eventdata,guidata(hObject)),...
'Tag','sub_final',...
'KeyPressFcn',@(hObject,eventdata)subjectInfo('sub_final_KeyPressFcn',hObject,eventdata,guidata(hObject)),...
'FontSize',12,...
'FontName','Arial',...
'CreateFcn', {@local_CreateFcn, blanks(0), appdata} );

appdata = [];
appdata.lastValidTag = 'name';

h9 = uicontrol(...
'Parent',h2,...
'FontUnits',get(0,'defaultuicontrolFontUnits'),...
'Units','normalized',...
'HorizontalAlignment',get(0,'defaultuicontrolHorizontalAlignment'),...
'String','Yang Zhang',...
'Style','edit',...
'Position',[0.404825737265416 0.853896103896104 0.294906166219839 0.0844155844155844],...
'BackgroundColor',bkColor,...
'Callback',@(hObject,eventdata)subjectInfo('name_Callback',hObject,eventdata,guidata(hObject)),...
'Children',[],...
'CreateFcn', {@local_CreateFcn, @(hObject,eventdata)subjectInfo('name_CreateFcn',hObject,eventdata,guidata(hObject)), appdata} ,...
'Tag','name',...
'FontSize',12,...
'FontName','Arial');

appdata = [];
appdata.lastValidTag = 'age';

h10 = uicontrol(...
'Parent',h2,...
'FontUnits',get(0,'defaultuicontrolFontUnits'),...
'Units','normalized',...
'String','22',...
'Style','edit',...
'Position',[0.404825737265416 0.717532467532468 0.294906166219839 0.0844155844155844],...
'BackgroundColor',bkColor,...
'Callback',@(hObject,eventdata)subjectInfo('age_Callback',hObject,eventdata,guidata(hObject)),...
'Children',[],...
'CreateFcn', {@local_CreateFcn, @(hObject,eventdata)subjectInfo('age_CreateFcn',hObject,eventdata,guidata(hObject)), appdata} ,...
'Tag','age',...
'FontSize',12,...
'FontName','Arial');

appdata = [];
appdata.lastValidTag = 'text5';

h11 = uicontrol(...
'Parent',h2,...
'FontUnits',get(0,'defaultuicontrolFontUnits'),...
'Units','normalized',...
'String','Designed by Yang Zhang, Psy, Soochow University',...
'Style','text',...
'Position',[0.0241286863270778 0.012987012987013 0.970509383378016 0.0551948051948052],...
'BackgroundColor',bkColor,...
'Children',[],...
'Tag','text5',...
'FontSize',10,...
'FontName','Arial',...
'CreateFcn', {@local_CreateFcn, blanks(0), appdata} );

appdata = [];
appdata.lastValidTag = 'text6';

h12 = uicontrol(...
'Parent',h2,...
'FontUnits',get(0,'defaultuicontrolFontUnits'),...
'Units','normalized',...
'String','SubjectNum:',...
'Style','text',...
'Position',[0.0134048257372654 0.288961038961039 0.281501340482574 0.064935064935065],...
'BackgroundColor',bkColor,...
'Children',[],...
'Tag','text6',...
'FontSize',12,...
'FontName','Arial',...
'CreateFcn', {@local_CreateFcn, blanks(0), appdata} );

appdata = [];
appdata.lastValidTag = 'num';

h13 = uicontrol(...
'Parent',h2,...
'FontUnits',get(0,'defaultuicontrolFontUnits'),...
'Units','normalized',...
'String','22',...
'Style','edit',...
'Position',[0.292225201072386 0.279220779220779 0.171581769436997 0.0844155844155844],...
'BackgroundColor',bkColor,...
'Callback',@(hObject,eventdata)subjectInfo('num_Callback',hObject,eventdata,guidata(hObject)),...
'Children',[],...
'CreateFcn', {@local_CreateFcn, @(hObject,eventdata)subjectInfo('num_CreateFcn',hObject,eventdata,guidata(hObject)), appdata} ,...
'Tag','num',...
'FontSize',12,...
'FontName','Arial');

appdata = [];
appdata.lastValidTag = 'text7';

h14 = uicontrol(...
'Parent',h2,...
'FontUnits',get(0,'defaultuicontrolFontUnits'),...
'Units','normalized',...
'String','Session:',...
'Style','text',...
'Position',[0.525469168900804 0.288961038961039 0.187667560321716 0.0616883116883117],...
'BackgroundColor',bkColor,...
'Children',[],...
'Tag','text7',...
'FontSize',12,...
'FontName','Arial',...
'CreateFcn', {@local_CreateFcn, blanks(0), appdata} );

appdata = [];
appdata.lastValidTag = 'session';

h15 = uicontrol(...
'Parent',h2,...
'FontUnits',get(0,'defaultuicontrolFontUnits'),...
'Units','normalized',...
'String','1',...
'Style','edit',...
'Position',[0.71313672922252 0.280130293159609 0.171581769436997 0.0844155844155844],...
'BackgroundColor',bkColor,...
'Callback',@(hObject,eventdata)subjectInfo('session_Callback',hObject,eventdata,guidata(hObject)),...
'Children',[],...
'CreateFcn', {@local_CreateFcn, @(hObject,eventdata)subjectInfo('session_CreateFcn',hObject,eventdata,guidata(hObject)), appdata} ,...
'Tag','session',...
'FontSize',12,...
'FontName','Arial');

appdata = [];
appdata.lastValidTag = 'hand';

h16 = uicontrol(...
'Parent',h2,...
'FontUnits',get(0,'defaultuicontrolFontUnits'),...
'Units','normalized',...
'String',{  'left'; 'right' },...
'Style','popupmenu',...
'Value',1,...
'Position',[0.404825737265416 0.435064935064935 0.294906166219839 0.0844155844155844],...
'BackgroundColor',bkColor,...
'Callback',@(hObject,eventdata)subjectInfo('hand_Callback',hObject,eventdata,guidata(hObject)),...
'Children',[],...
'ButtonDownFcn',@(hObject,eventdata)subjectInfo('hand_ButtonDownFcn',hObject,eventdata,guidata(hObject)),...
'CreateFcn', {@local_CreateFcn, @(hObject,eventdata)subjectInfo('hand_CreateFcn',hObject,eventdata,guidata(hObject)), appdata} ,...
'Tag','hand',...
'FontSize',12,...
'FontName','Arial');

appdata = [];
appdata.lastValidTag = 'gender';

h17 = uicontrol(...
'Parent',h2,...
'FontUnits',get(0,'defaultuicontrolFontUnits'),...
'Units','normalized',...
'HorizontalAlignment',get(0,'defaultuicontrolHorizontalAlignment'),...
'String',{  'male'; 'female' },...
'Style','popupmenu',...
'Value',1,...
'Position',[0.404825737265416 0.568181818181818 0.294906166219839 0.0844155844155844],...
'BackgroundColor',bkColor,...
'Callback',@(hObject,eventdata)subjectInfo('gender_Callback',hObject,eventdata,guidata(hObject)),...
'Children',[],...
'CreateFcn', {@local_CreateFcn, @(hObject,eventdata)subjectInfo('gender_CreateFcn',hObject,eventdata,guidata(hObject)), appdata} ,...
'Tag','gender',...
'FontSize',12,...
'FontName','Arial');


hsingleton = h1;


% --- Set application data first then calling the CreateFcn. 
function local_CreateFcn(hObject, eventdata, createfcn, appdata)

if ~isempty(appdata)
   names = fieldnames(appdata);
   for i=1:length(names)
       name = char(names(i));
       setappdata(hObject, name, getfield(appdata,name));
   end
end

if ~isempty(createfcn)
   if isa(createfcn,'function_handle')
       createfcn(hObject, eventdata);
   else
       eval(createfcn);
   end
end


% --- Handles default GUIDE GUI creation and callback dispatch
function varargout = gui_mainfcn(gui_State, varargin)

gui_StateFields =  {'gui_Name'
    'gui_Singleton'
    'gui_OpeningFcn'
    'gui_OutputFcn'
    'gui_LayoutFcn'
    'gui_Callback'};
gui_Mfile = '';
for i=1:length(gui_StateFields)
    if ~isfield(gui_State, gui_StateFields{i})
        error(message('MATLAB:guide:StateFieldNotFound', gui_StateFields{ i }, gui_Mfile));
    elseif isequal(gui_StateFields{i}, 'gui_Name')
        gui_Mfile = [gui_State.(gui_StateFields{i}), '.m'];
    end
end

numargin = length(varargin);

if numargin == 0
    % SUBJECTINFO
    % create the GUI only if we are not in the process of loading it
    % already
    gui_Create = true;
elseif local_isInvokeActiveXCallback(gui_State, varargin{:})
    % SUBJECTINFO(ACTIVEX,...)
    vin{1} = gui_State.gui_Name;
    vin{2} = [get(varargin{1}.Peer, 'Tag'), '_', varargin{end}];
    vin{3} = varargin{1};
    vin{4} = varargin{end-1};
    vin{5} = guidata(varargin{1}.Peer);
    feval(vin{:});
    return;
elseif local_isInvokeHGCallback(gui_State, varargin{:})
    % SUBJECTINFO('CALLBACK',hObject,eventData,handles,...)
    gui_Create = false;
else
    % SUBJECTINFO(...)
    % create the GUI and hand varargin to the openingfcn
    gui_Create = true;
end

if ~gui_Create
    % In design time, we need to mark all components possibly created in
    % the coming callback evaluation as non-serializable. This way, they
    % will not be brought into GUIDE and not be saved in the figure file
    % when running/saving the GUI from GUIDE.
    designEval = false;
    if (numargin>1 && ishghandle(varargin{2}))
        fig = varargin{2};
        while ~isempty(fig) && ~ishghandle(fig,'figure')
            fig = get(fig,'parent');
        end
        
        designEval = isappdata(0,'CreatingGUIDEFigure') || (isscalar(fig)&&isprop(fig,'GUIDEFigure'));
    end
        
    if designEval
        beforeChildren = findall(fig);
    end
    
    % evaluate the callback now
    varargin{1} = gui_State.gui_Callback;
    if nargout
        [varargout{1:nargout}] = feval(varargin{:});
    else       
        feval(varargin{:});
    end
    
    % Set serializable of objects created in the above callback to off in
    % design time. Need to check whether figure handle is still valid in
    % case the figure is deleted during the callback dispatching.
    if designEval && ishghandle(fig)
        set(setdiff(findall(fig),beforeChildren), 'Serializable','off');
    end
else
    if gui_State.gui_Singleton
        gui_SingletonOpt = 'reuse';
    else
        gui_SingletonOpt = 'new';
    end

    % Check user passing 'visible' P/V pair first so that its value can be
    % used by oepnfig to prevent flickering
    gui_Visible = 'auto';
    gui_VisibleInput = '';
    for index=1:2:length(varargin)
        if length(varargin) == index || ~ischar(varargin{index})
            break;
        end

        % Recognize 'visible' P/V pair
        len1 = min(length('visible'),length(varargin{index}));
        len2 = min(length('off'),length(varargin{index+1}));
        if ischar(varargin{index+1}) && strncmpi(varargin{index},'visible',len1) && len2 > 1
            if strncmpi(varargin{index+1},'off',len2)
                gui_Visible = 'invisible';
                gui_VisibleInput = 'off';
            elseif strncmpi(varargin{index+1},'on',len2)
                gui_Visible = 'visible';
                gui_VisibleInput = 'on';
            end
        end
    end
    
    % Open fig file with stored settings.  Note: This executes all component
    % specific CreateFunctions with an empty HANDLES structure.

    
    % Do feval on layout code in m-file if it exists
    gui_Exported = ~isempty(gui_State.gui_LayoutFcn);
    % this application data is used to indicate the running mode of a GUIDE
    % GUI to distinguish it from the design mode of the GUI in GUIDE. it is
    % only used by actxproxy at this time.   
    setappdata(0,genvarname(['OpenGuiWhenRunning_', gui_State.gui_Name]),1);
    if gui_Exported
        gui_hFigure = feval(gui_State.gui_LayoutFcn, gui_SingletonOpt);

        % make figure invisible here so that the visibility of figure is
        % consistent in OpeningFcn in the exported GUI case
        if isempty(gui_VisibleInput)
            gui_VisibleInput = get(gui_hFigure,'Visible');
        end
        set(gui_hFigure,'Visible','off')

        % openfig (called by local_openfig below) does this for guis without
        % the LayoutFcn. Be sure to do it here so guis show up on screen.
        movegui(gui_hFigure,'onscreen');
    else
        gui_hFigure = local_openfig(gui_State.gui_Name, gui_SingletonOpt, gui_Visible);
        % If the figure has InGUIInitialization it was not completely created
        % on the last pass.  Delete this handle and try again.
        if isappdata(gui_hFigure, 'InGUIInitialization')
            delete(gui_hFigure);
            gui_hFigure = local_openfig(gui_State.gui_Name, gui_SingletonOpt, gui_Visible);
        end
    end
    if isappdata(0, genvarname(['OpenGuiWhenRunning_', gui_State.gui_Name]))
        rmappdata(0,genvarname(['OpenGuiWhenRunning_', gui_State.gui_Name]));
    end

    % Set flag to indicate starting GUI initialization
    setappdata(gui_hFigure,'InGUIInitialization',1);

    % Fetch GUIDE Application options
    gui_Options = getappdata(gui_hFigure,'GUIDEOptions');
    % Singleton setting in the GUI MATLAB code file takes priority if different
    gui_Options.singleton = gui_State.gui_Singleton;

    if ~isappdata(gui_hFigure,'GUIOnScreen')
        % Adjust background color
        if gui_Options.syscolorfig
            set(gui_hFigure,'Color', get(0,'DefaultUicontrolBackgroundColor'));
        end

        % Generate HANDLES structure and store with GUIDATA. If there is
        % user set GUI data already, keep that also.
        data = guidata(gui_hFigure);
        handles = guihandles(gui_hFigure);
        if ~isempty(handles)
            if isempty(data)
                data = handles;
            else
                names = fieldnames(handles);
                for k=1:length(names)
                    data.(char(names(k)))=handles.(char(names(k)));
                end
            end
        end
        guidata(gui_hFigure, data);
    end

    % Apply input P/V pairs other than 'visible'
    for index=1:2:length(varargin)
        if length(varargin) == index || ~ischar(varargin{index})
            break;
        end

        len1 = min(length('visible'),length(varargin{index}));
        if ~strncmpi(varargin{index},'visible',len1)
            try set(gui_hFigure, varargin{index}, varargin{index+1}), catch break, end
        end
    end

    % If handle visibility is set to 'callback', turn it on until finished
    % with OpeningFcn
    gui_HandleVisibility = get(gui_hFigure,'HandleVisibility');
    if strcmp(gui_HandleVisibility, 'callback')
        set(gui_hFigure,'HandleVisibility', 'on');
    end

    feval(gui_State.gui_OpeningFcn, gui_hFigure, [], guidata(gui_hFigure), varargin{:});

    if isscalar(gui_hFigure) && ishghandle(gui_hFigure)
        % Handle the default callbacks of predefined toolbar tools in this
        % GUI, if any
        guidemfile('restoreToolbarToolPredefinedCallback',gui_hFigure); 
        
        % Update handle visibility
        set(gui_hFigure,'HandleVisibility', gui_HandleVisibility);

        % Call openfig again to pick up the saved visibility or apply the
        % one passed in from the P/V pairs
        if ~gui_Exported
            gui_hFigure = local_openfig(gui_State.gui_Name, 'reuse',gui_Visible);
        elseif ~isempty(gui_VisibleInput)
            set(gui_hFigure,'Visible',gui_VisibleInput);
        end
        if strcmpi(get(gui_hFigure, 'Visible'), 'on')
            figure(gui_hFigure);
            
            if gui_Options.singleton
                setappdata(gui_hFigure,'GUIOnScreen', 1);
            end
        end

        % Done with GUI initialization
        if isappdata(gui_hFigure,'InGUIInitialization')
            rmappdata(gui_hFigure,'InGUIInitialization');
        end

        % If handle visibility is set to 'callback', turn it on until
        % finished with OutputFcn
        gui_HandleVisibility = get(gui_hFigure,'HandleVisibility');
        if strcmp(gui_HandleVisibility, 'callback')
            set(gui_hFigure,'HandleVisibility', 'on');
        end
        gui_Handles = guidata(gui_hFigure);
    else
        gui_Handles = [];
    end

    if nargout
        [varargout{1:nargout}] = feval(gui_State.gui_OutputFcn, gui_hFigure, [], gui_Handles);
    else
        feval(gui_State.gui_OutputFcn, gui_hFigure, [], gui_Handles);
    end

    if isscalar(gui_hFigure) && ishghandle(gui_hFigure)
        set(gui_hFigure,'HandleVisibility', gui_HandleVisibility);
    end
end

function gui_hFigure = local_openfig(name, singleton, visible)

% openfig with three arguments was new from R13. Try to call that first, if
% failed, try the old openfig.
if nargin('openfig') == 2
    % OPENFIG did not accept 3rd input argument until R13,
    % toggle default figure visible to prevent the figure
    % from showing up too soon.
    gui_OldDefaultVisible = get(0,'defaultFigureVisible');
    set(0,'defaultFigureVisible','off');
    gui_hFigure = matlab.hg.internal.openfigLegacy(name, singleton);
    set(0,'defaultFigureVisible',gui_OldDefaultVisible);
else
    % Call version of openfig that accepts 'auto' option"
    gui_hFigure = matlab.hg.internal.openfigLegacy(name, singleton, visible);  
%     %workaround for CreateFcn not called to create ActiveX
%         peers=findobj(findall(allchild(gui_hFigure)),'type','uicontrol','style','text');    
%         for i=1:length(peers)
%             if isappdata(peers(i),'Control')
%                 actxproxy(peers(i));
%             end            
%         end
end

function result = local_isInvokeActiveXCallback(gui_State, varargin)

try
    result = ispc && iscom(varargin{1}) ...
             && isequal(varargin{1},gcbo);
catch
    result = false;
end

function result = local_isInvokeHGCallback(gui_State, varargin)

try
    fhandle = functions(gui_State.gui_Callback);
    result = ~isempty(findstr(gui_State.gui_Name,fhandle.file)) || ...
             (ischar(varargin{1}) ...
             && isequal(ishghandle(varargin{2}), 1) ...
             && (~isempty(strfind(varargin{1},[get(varargin{2}, 'Tag'), '_'])) || ...
                ~isempty(strfind(varargin{1}, '_CreateFcn'))) );
catch
    result = false;
end


