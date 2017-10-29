%% Initialization of global variables
% Define the parameters of the equation $Ax + By = C$
A = 17;
B = 12;
C = 6;
dist = @(walker)(abs(C - A*walker(1) - B*walker(2)));

% Define the possible moves and the associated weights;
% Set the walker to start at (0, 0) and compute the distance
% Set alpha to be the regulating parameter of the weights
moves = {[1,0], [1,1], [0,1], [-1,1], [-1,0], [-1,-1], [0,-1], [1,-1]};
weights = ones(1, length(moves));
alpha = 1.1;
walker = [0, 0];
d = dist(walker);

its = 1;
maxiterations = 1000;
% store the positions and distances to plot in the end
walk = zeros(maxiterations, 2);
d_walk = zeros(maxiterations, 1);

%% Simulation

while its <= maxiterations && d > 0
    % Pick the move the walker will make
    parts = generatePartition(weights);
    m = pickSubinterval(parts);
    walker = walker + moves{m};
    
    % Find if the position of the walker improved and adjust weights
    if dist(walker) < d
        weights(m) = weights(m)*alpha;
    else
        weights(m) = weights(m)/alpha;
    end;
    
    % Store the new position and new distance
    walk(its, :) = walker;
    d = dist(walker);
    d_walk(its) = d;
    its = its + 1;
end;

%% Result plotting

% Plot the 2D walk, the evolution of the distance with the number of
%   iterations and the distance in terms of the position
figure(1);
plot(walk(1:its-1, 1), walk(1:its-1, 2));
title('2D Random Walk'); xlabel('X'); ylabel('Y');
figure(2);
plot(1:its-1, d_walk(1:its-1));
title('Evolution of d with time'); xlabel('iterations'); ylabel('d');
figure(3);
plot3(walk(1:its-1, 1), walk(1:its-1, 2), d_walk(1:its-1));
title('d for each position'); xlabel('X'); ylabel('Y'); zlabel('d');