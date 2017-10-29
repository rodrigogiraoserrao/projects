function [intervals] = generatePartition(weights)
    %% Given a vector of weights, creates a partition of the
    %%% [0,1] interval such that the subintervals' lengths have,
    %%% between themselves, the same proportions as the weights.
    n = length(weights);
    % normalize the weights with the L1 norm
    weights = weights / norm(weights, 1);
    sizes = ones(1, n).*weights;
    intervals = sizes;
    for i = 2:n
        intervals(i:end) = intervals(i:end) + sizes(i-1);
    end;
end