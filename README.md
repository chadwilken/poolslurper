# PoolSlurper

## What it do?
This is a simple python script that grabs, every 5 minutes, the *estimated* profits for various mining algorithms from a few cryptocurrency mining pools' API data. It saves the data in .csv files by appending to the template files in the csvdata folder.

For pools that support it, it also grabs their reported "actual" profits.

## Why?
These pools offer auto-exchange, so you can mine whatever algorithm you want, and get payout in a single, preferred cryptocurrency (with some limits for some pools).

Commonly one mines with a program that switches algorithms automatically, such as MultiPoolMiner, AwesomeMiner, etc. (I even wrote my own imperfect, buggy cross-platform python multi-miner that I doubt I'll ever publish because I don't have enough time to support questions, but -- you get the idea.)

Some people report that it's better to just stick to one algorithm on one pool rather than switching all the time.

This got me curious -- which algorithm? Which pool? Or if one still wants to switch, perhaps a small group of algorithms could be seen to perform "best" over time?

## What's the results?
As of March 2, 2018, I ran this on my own server for a week, from about Feb 21 to Mar 1. I collated that data into the MS Excel spreadsheets in the dated results folder.

First, some explanation on the spreadsheets, then some inexpert data analysis...

### General spreadsheet info
The spreadsheets both contain the following:

* summary tab of all algorithm averages for all pools
* hashrates tab -- you should enter hashrates for your hardware here (the pre-filled data is from a single GeForce GTX 1070)
* tabs for charts & calculation tables. The charts I have initially filtered to the top algorithms for each pool. The calculation tables use the hashrate data to determine profits from the pool-reported estimate/actual data. These calculations take into account pool fees where applicable, except Nicehash because that's more complicated.
* raw data tabs. If you wanted to run the script yourself and add new data or replace the data, this is where you'd want to put raw data. (You'll also then have to resize the calculation tables so they pick up whatever different quantity of data you're working with.)

The "estimate" spreadsheet uses the pool estimated profits data. The "actual" spreadsheet uses the pool-reported "actual" data, which is not available for Nicehash or MiningPoolHub, so they aren't in the "actual" spreadsheet.

Please note that all this data is reported by the pools and may not be accurate. I did no tests to verify this, I just slurped the pools' data.

### My analysis
I grabbed data for one week. One can already see in that data that there's a lot of fluctuation (like lyra2v2 in the blazepool "actual" data).

In both the estimate & actual data, it seems the best pool & algorithm combination is neoscrypt at zergpool. That said, I've experienced a *lot* of connection problems with zergpool recently, so this might not work out so great.

Next is blazepool, which shows neoscrypt on top for estimates, but lyra2v2 on top for actual returns during the sample period. I've not used blazepool myself but it seems like a good performer even with fees!

I would note here that the "actual" data differs from the "estimates," and I think the multi-pool switching software like MultiPoolMiner usually uses the "estimate" data to decide what to mine. So in this example, blazepool reported relatively consistent estimates for neoscrypt & lyra2v2, but lyra2v2 actual profits fluctuated wildly, and ended the week with a higher return on average, according to the pool data.

Zpool seems 3rd in the runnings. It seems the phi algorithm had a good week there -- but again, the week's estimates for phi were relatively low and steady while the actual fluctuated wildly, so, if accurate, your switching software might not have been switching to phi, yet it was getting better returns for some periods.

Ahashpool also favored neoscrypt for both estimate & actual data, followed by x17 for estimates, but xevan for actual.

Nicehash & MiningPoolHub both saw equihash as favorites, but the estimate returns are much lower than neoscrypt at the other pools, even with fees factored in. And if you favor a little switching, lyra2v2 and neoscrypt also did well at Nicehash & MiningPoolHub.

### Conclusion
I'm no skilled analyst, sorry! But maybe this will help some of you narrow down what's most profitable for your hardware and preferred pools, and prevent some needless switching.

When algorithms spike, they don't seem to spike for long. It seems really inefficient and difficult to try to switch too often, always hoping to catch a spike before it falls.

We can see in the "actual" data that there are smoother, longer upturns, but those are hard to predict and we don't see it in the estimate data that usually actually drives switching.

So it really does seem better to pick one or two reliable algorithms at a good pool and stick to them -- which generally seems to be neoscrypt, except for Nicehash & MiningPoolHub where it's equihash.

## Tips
This seems silly but if anyone wants, I'll take tips...

BTC: 35Vz5g6RaBXZSwSUceeunsqtrc8r7viKZJ
LTC: LZgsfMQhPCxwJV71TtmuHgQGtoEGG4xidw
ETH: 0x8283f38a399b1bd48e9fe9aab49afdb8b3a86d3b
