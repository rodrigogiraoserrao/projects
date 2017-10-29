%% Initialization of global variables
% Define the possible moves and the associated weights;
% Set alpha to be the regulating parameter of the weights
moves = combvec([-1,0,1], [-1,0,1], [-1,0,1]);
% find the 0 vector to remove it
i = find((moves(1,:)==0).*(moves(2,:)==0).*(moves(3,:)==0));
moves = moves(:, [(1:i-1) (i+1:27)])';
alpha = 1.1;
% set how many independent walkers are to be used for each n
howManyWalkers = 3;
maxiterations = 1000;
% flag if the final plots are to be plotted
% set to false if n is going over a big range of numbers
finalPlots = false;

for n = 2:25
    fprintf('N = %d \n', n);
    % Define the distance
    dist = @(w)(abs(4/n - sum(1./w)));

    % Set the walker to start at (2, 2, 2) and compute the distance
    walkers = 2*ones(howManyWalkers, 3);
    d = dist(walkers(1,:))*ones(1, howManyWalkers);
    best_d = d(1);
    weights = ones(howManyWalkers, length(moves));

    its = 1;
    % store the positions and distances to plot in the end
    walk = zeros(maxiterations, 3, howManyWalkers);
    d_walk = zeros(maxiterations, howManyWalkers);
    best = [inf, inf, inf];

    %% Simulation
    while its <= maxiterations && best_d > 10^(-7)
        for j = 1:howManyWalkers
            % Pick the move the walker will make
            parts = generatePartition(weights(j, :));
            m = pickSubinterval(parts);
            % stay in the positive numbers
            while ~prod((walkers(j, :) + moves(m, :)) > 0)
                m = pickSubinterval(parts);
            end;
            walkers(j, :) = walkers(j, :) + moves(m, :);

            % Find if the position of the walker improved and adjust weights
            if dist(walkers(j, :)) < d(j)
                weights(j, m) = weights(j, m)*alpha;
            else
                weights(j, m) = weights(j, m)/alpha;
            end;

            % Store the new position and new distance if needed
            walk(its, :, j) = walkers(j, :);
            d_walk(its, j) = dist(walkers(j, :));
            d(j) = d_walk(its, j);
            if d(j) < best_d
                best_d = d(j);
                best = walkers(j, :);
            end;
        end;
        its = its + 1;
    end;

    %% Result plotting

    if finalPlots
        % Plot the 3D walk, the evolution of the distance with the number of
        %   iterations and the distance in terms of the position
        figure; hold on;
        for j = 1:howManyWalkers
            plot(1:its-1, d_walk(1:its-1, j));
        end
        title('Evolution of d with time'); xlabel('iterations'); ylabel('d');
        hold off;

        figure; hold on;
        for j = 1:howManyWalkers
            plot3(walk(1:its-1, 1, j), walk(1:its-1, 2, j), walk(1:its-1, 3, j));
        end
        title('Evolution of the positions'); xlabel('X'); ylabel('Y'); zlabel('Z');
        hold off;

        figure; hold on;
        for j = 1:howManyWalkers
            plot3(walk(1:its-1, 1, j), walk(1:its-1, 2, j), walk(1:its-1, 3, j));
            scatter3(walk(1:its-2, 1, j), walk(1:its-2, 2, j), walk(1:its-2, 3, j), 100*d_walk(1:its-2, j)');
        end
        title('Evolution of the positions and d'); xlabel('X'); ylabel('Y'); zlabel('Z');
        hold off;
    end;
        
    % Say if we found a solution or present the best approximation
    if best_d == 0
        fprintf('\tFound a solution (%d, %d, %d) in %d iterations\n', best(1), best(2), best(3), its);
    else
        fprintf('\tWas looking for %.4f\n', 4/n);
        fprintf('\tFound %.4f at (%d, %d, %d)\n',sum(1./best),best(1),best(2),best(3));
    end;
end