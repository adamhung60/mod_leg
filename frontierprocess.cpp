

frontier_processing_t plan_path_to_frontier(const std::vector<frontier_t>& frontiers,
                                            const mbot_msg::msg::Pose2dt& robotPose,
                                            const OccupancyGrid& map,
                                            const MotionPlanner& planner)
{
    ///////////// TODO: Implement your strategy to select the next frontier to explore here //////////////////

    // First, choose the frontier to go to
    // Initial alg: find the nearest one

    // Returnable path
    mbot_msg::msg::Path2dt path;
    path.utime = utime_now();
    path.path_length = 1;
    path.path.push_back(robotPose);

    /**
     * In this function, you should implement a frontier selection policy. It might not be that the frontiers are
     * available to travel to, due to not being in the configuration space, so you should find the nearest cell to the
     * frontier that is navigable. The current implementation attempts to navigate to the nearest centroid of a frontier,
     * but this is not a good policy, as the robot might not be able to navigate to the centroid. Instead, you should
     * come with a stretegy to navigate to the nearest navigable of the frontier.
     * TODO:
     *  - Find the centroid of each frontier using the find_frontier_centroid function and store it in a vector
     *  - Sort the centroids by distance
     *      - Hint: use the CompareCentroids struct and std::sort();
     *  - Perform a search to the nearest free space cell for each centroid
     *  - If the search is successful, then plan a path to the centroid and assign it to the path variable
     *  - If the search is unsuccessful, add 1 to the unreachable_frontiers counter.
     *  - Return the frontier_processing_t structure
     *      - i.e return frontier_processing_t(path, unreachable_frontiers);
     */

    // Keeping count of the number of cells that the robot cannot get to
    int unreachable_frontiers = 0;

    // Keep track of whether a valid cell to travel to is found
    bool found_valid_cell = false;

    // Point to store the nearest cell to the frontier that is navigable
    Point<double> goal;


    // Get the centroids of every frontier, and sort them in ascending order by distance to the robot
    frontier_t chosen_frontier;
    std::vector<Point<double>> centroids;
    for (auto &&frontier : frontiers)
    {
        // Find the centroid of the frontier
        auto centroid = find_frontier_centroid(frontier);
        centroids.push_back(centroid);
    }
    
    // Order the centroids by their distance to the robot
    std::sort(centroids.begin(), centroids.end(), CompareCentroids(robotPose));
    
    
    
    /**
     * Perform a search to the nearest free space cell for each centroid. 
     * Here, we will give a strategy for this search:
     *  1) Use a radial search, centered at the centroid, to find the nearest free space cell
     *      - The radial search uses the strategy of taking steps in incrementing angles (directions) around the centroid.
     *        If all the directions are checked and no free space cell is found, then take a larger step in the radial direction and repeat
     *      - In order to perform this, you will need to specify the number of directions to check and the number of steps to take in the radial direction
     *          i.e. int num_directions = 8; int num_radial_steps = 5; int radial_increments = 1;
     *      - For a selected number of directions, the directions can be computed as follows:
     *          float angle = 2 * M_PI / num_directions * i; where i is the direction index
     *          direction = Point<double>(cos(angle), sin(angle));
     *      - To then perform the radial search:
     *          1) Iterate through each centroid
     *          2) Find the centriod_cell in the grid by using the global_position_to_grid_cell function
     *          3) Iterate through the number of radial steps.
     *              This can be done with a while loop that checks that check !found_valid_cell && radial_step <= num_radial_steps
     *          4) Iterate through the directions
     *          5) Define a cell_t with the current radial step and direction
     *              i.e. cell_t cell = (centroid_cell.x + radius * direction.x, centroid_cell.y + radius * direction.y);
     *          6) Check if the cell is in the grid and if it is free space. If not, skip to the next direction
     *          7) If the cell is a valid goal (check using planner.isValidGoal()), that means a path can be planned to it!
     *              - Set the goal to the global position of the cell
     *              - Set found_valid_cell to true
     *              - Define a pose_xyt_t with the goal cell x and y. Set the theta = 0 and the utime = utime_now()
     *              - Plan a path to the goal using the planner.planPath() function
     *              - If the path is valid (the length of the path will be greater than 1) and safe, break from the directions loop
     *              - If the path is not valid, then set found_valid_cell to false and continue to the next direction
     *              - Make sure to increment the radial_step at the end of the directions loop
     *              - Once out of the radial loop, check if found_valid_cell is true. If it is, break from the centroid loop. this means a valid path was found
     *              - If found_valid_cell is false, then increment the unreachable_frontiers counter
     *          8) Finally, return the path that was found and the number of unreachable frontiers (frontier_processing_t(path, unreachable_frontiers))
     *  2) A BFS search by radially expanding to the 4 directions from the centroid. This would require using a queue to store the cells to check.
     */


    // We highly recommend replacing this with your own implementation for an alternate search method, as this is not a good policy
    
    // Uncomment or replace while implementing
    /*
    for (auto &&c : centroids)
    {
        // Find the closest cell that is a valid goal
        // Do a breadth first search 4 way
        Point<int> centr_cell = global_position_to_grid_cell(c, map);
        // printf("centroid (%d,%d)\n", centr_cell.x, centr_cell.y);

        // This will mark how many cells from the initial one are we. We can stop searching if we get to a certain value
        int counter_dist = 1;
        // Step to accelerate the finding
        int distance_step = 1;

        Point<int> goal_cell;
        auto centr_directions = directions;

        while (!found_valid_cell && counter_dist <= max_counter_dist)
        {
            for (auto &&dir : centr_directions)
            {
                // printf("dir: (%d,%d)\n", dir.first, dir.second);
                // Way to block certain directions
                if (dir.first == 0.0 && dir.second == 0.0)
                    continue;

                cell_t new_cell(
                    centr_cell.x + dir.first * counter_dist,
                    centr_cell.y + dir.second * counter_dist
                );
                // printf("new cell: (%d,%d)\n", new_cell.x, new_cell.y);
                // Check if cell is a wall. Block that direction
                if (map.isCellInGrid(new_cell.x, new_cell.y) && map.logOdds(new_cell.x, new_cell.y) > 0)
                {
                    dir = std::pair<float,float>(0.0,0.0);
                    continue;
                }

                // Check if it is a valid goal
                if (planner.isValidGoal(new_cell))
                {
                    goal_cell = new_cell;
                    found_valid_cell = true;
                    goal = grid_position_to_global_position(goal_cell, map);
                    mbot_msg::msg::Pose2dt goal_pose;
                    goal_pose.x = goal.x;
                    goal_pose.y = goal.y;
                    goal_pose.theta = 0.0;
                    goal_pose.utime = utime_now();

                    // printf("goal (%f,%f)\n", goal.x, goal.y);
                    // Plan the path to that chosen centroid
                    path = planner.planPath(robotPose, goal_pose);
                    // Only end the processing if it found a valid path
                    if (path.path_length > 1)
                        break;
                    else
                        found_valid_cell = false;
                }
            }

            counter_dist++;
        }
        if (found_valid_cell)
        {
            break;
        }
        if (!found_valid_cell)
        {
            // printf("was unreachable\n");
            unreachable_frontiers++;
        }
    }
    */

    return frontier_processing_t(path, unreachable_frontiers);
}
