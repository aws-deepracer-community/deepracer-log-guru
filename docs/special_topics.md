# Special Topics

## Obstacle Avoidance
The default log file output from Deep Racer does not contain information about the location of obstacles. However Deep Racer Guru can currently analyze **static** obstacle avoidance **if** you provide the extra information in your reward function.

If you are using the DRF (Deep Racer Framework) then this is already done for you.

But if you using a bespoke reward function, or any other framework or library, then you must add the following lines into your reward function:

        if params['steps'] == 2:
            print("DRG-OBJECTS:", params['objects_location'])
                        
## Testing a New Reward Function
TODO

## Testing Different Discount Factors
TODO



## Parsing Debug Output
TODO
