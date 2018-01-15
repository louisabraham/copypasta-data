# copypasta-data

I provide scripts to scrape:

    - https://twitch.gimu.org/
    - https://www.twitchquotes.com/copypastas
    - https://www.reddit.com/r/copypasta/top/?sort=top&t=all

as well as their output.

They print the copypastas written with only ASCII characters to limit
the dimension of the dataset.

For an unknown reason, lxml cannot parse very well the html from twitchquotes.com,
and it is very slow with html5lib, so the script takes about 2 minutes.
twitch.gimu.org is scraped in 15 seconds thanks to parallel download.
I could not find more than 39 pages of /r/copypasta, they were downloaded in less than 3 minutes.

I also provide their output as it was generated today with

    ./twitch_copypasta_async.py > copypasta.txt
    ./twitchquotes.py > copypasta2.txt
    ./copypasta_reddit.py -1 > reddit.txt

# LSTM for copypasta generation

I slightly modified the keras example `lstm_text_generation.py`
available [here](https://github.com/keras-team/keras/blob/master/examples/lstm_text_generation.py)
to run on our dataset.

The original learning rate of 0.01 really hurts the performance, the default value
of 0.001 yields much better results.

If you have keras installed, just run `./copypasta.py`

# TODO

Use a better model with more layers, validation and dropout.