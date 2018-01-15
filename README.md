copypasta-data
==============

I provide scripts to scrape copypastas from:

-   https://twitch.gimu.org/
-   https://www.twitchquotes.com/copypastas
-   https://www.reddit.com/r/copypasta/top/?sort=top&t=all

as well as their output.

They print the copypastas written with only ASCII characters to limit
the dimension of the dataset.

For an unknown reason, lxml cannot parse very well the html from
twitchquotes.com, and it is very slow with html5lib, so the script takes
about 2 minutes. twitch.gimu.org is scraped in 15 seconds thanks to
parallel download. I could not find more than 39 pages of /r/copypasta,
they were downloaded in less than 3 minutes.

I also provide their output as it was generated today with

    ./twitch_copypasta_async.py > copypasta.txt
    ./twitchquotes.py > copypasta2.txt
    ./copypasta_reddit.py -1 > reddit.txt

LSTM for copypasta generation
=============================

I modified the keras example `lstm_text_generation.py` available
[here](https://github.com/keras-team/keras/blob/master/examples/lstm_text_generation.py)
to run on our dataset.

I use two layers of Bidirectional GRU (Gated Recurrent Units) instead of LSTM, with .5
Dropout layers between them. Here is the summary:

    _________________________________________________________________
    Layer (type)                 Output Shape              Param #   
    =================================================================
    input_1 (InputLayer)         (None, 40, 92)            0         
    _________________________________________________________________
    bidirectional_1 (Bidirection (None, 40, 256)           169728    
    _________________________________________________________________
    dropout_1 (Dropout)          (None, 40, 256)           0         
    _________________________________________________________________
    bidirectional_2 (Bidirection (None, 128)               123264    
    _________________________________________________________________
    dropout_2 (Dropout)          (None, 128)               0         
    _________________________________________________________________
    dense_1 (Dense)              (None, 128)               16512     
    _________________________________________________________________
    dropout_3 (Dropout)          (None, 128)               0         
    _________________________________________________________________
    dense_2 (Dense)              (None, 92)                11868     
    _________________________________________________________________
    activation_1 (Activation)    (None, 92)                0         
    =================================================================
    Total params: 321,372
    Trainable params: 321,372
    Non-trainable params: 0
    _________________________________________________________________

If you have keras installed, just run `./copypasta.py`

References
==========

-   Andrej Karpathy, [The Unreasonable Effectiveness of Recurrent Neural
    Networks](https://karpathy.github.io/2015/05/21/rnn-effectiveness/)

-   Alex Graves, [Generating Sequences With Recurrent Neural
    Networks](https://arxiv.org/pdf/1308.0850.pdf)
