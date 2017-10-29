function [int] = pickSubinterval(partition)
    %% Receives a partition of the interval [0,1] and returns the index
    %%% of a random subinterval
    r = rand;
    int = 1;
    while r > partition(int)
        int = int + 1;
    end;
end
