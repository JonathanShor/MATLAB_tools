function [imData] = loadTiff(fname, stackSize)
%LOADTIFF Load greyscale TIFF image stack into a 3D array
% Inputs:
%   fname: Full file path and name of a tiff
%   stackSize: OPTIONAL. Number of images in the stack
% Outputs:
%   imData: Greyscale values. [image, x, y]
maxDirectory = 65536;
if nargin > 1
    maxDirectory = stackSize;
end

f = imread(fname,1);
%Assume first frame is maximal size for full stack
imData = zeros(maxDirectory, size(f,1), size(f,2), 'uint8');
imData(1,:,:) = f;
try
    for i_image = 2:maxDirectory
        imData(i_image, :, :) = imread(fname, i_image);
    end
catch ME
    switch ME.identifier
        case 'MATLAB:imagesci:rtifc:invalidDirIndex'
            imData = imData(1:i_image-1,:,:);
        otherwise
            rethrow(ME)
    end
end

end

