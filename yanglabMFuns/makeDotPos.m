function dotsData = makeDotPos(nDots,direction,pixsPerSec,coherence,isOval,w,h,dur,ifi)

nframes  = ceil(dur/ifi) + 3;
nCohDots = round(nDots*coherence);

dotsData = zeros(nDots,3,nframes); % rows: dotIndex; cols: x y isShow; layers: nframe 

directs  = repmat([repmat(direction,nCohDots,1);rand(nDots - nCohDots,1)],[1,1,nframes]);

steps    = reshape(1:nframes,[1,1,nframes]);

dotsData(:,1,:) = repmat(rand(nDots,1),[1,1,nframes])*w + repmat(steps*pixsPerSec*ifi,[nDots,1,1]).*cos(directs);
dotsData(:,2,:) = repmat(rand(nDots,1),[1,1,nframes])*h + repmat(steps*pixsPerSec*ifi,[nDots,1,1]).*sin(directs);

dotsData(:,1,:) = rem(dotsData(:,1,:),w) - w/2;
dotsData(:,2,:) = rem(dotsData(:,2,:),h) - h/2;

if isOval
	dotsData(:,3,:) = dotsData(:,1,:).^2/(w/2) + dotsData(:,2,:).^2/(h/2) <= 1; 
else
	dotsData(:,3,:) = 1;
end 

end