%matlab -nodisplay -nodesktop -r "run myfile.m"
clear; clc;

% --- single threaded run ---
% parpool; does nothing on this problem
% number of runs
runs = 10;
% number of data points
n = [1e6 1e7 1e8 1e9];
mean_run_times = zeros(4,1);
for j = 1:4
    time_plus_eq = zeros(runs,1);
    for i = 1:runs
        X = ones(n(j),1);
        Y = ones(n(j),1);
        t = cputime;
        %X = X + 2.0*Y;
        % interesting this is slower in matlab than X = X + 2.0*Y;
	X = X + Y + Y;
	%X = X + Y;
	e = cputime-t;
        time_plus_eq(i) = e;
    end
    mm = mean(time_plus_eq);
    mean_run_times(j) = mm;
end
mean_run_times
savefile = 'matlab_single.mat';
save(savefile, 'mean_run_times')
