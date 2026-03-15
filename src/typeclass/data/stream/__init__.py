from typeclass.data.stream.core import Stream
from typeclass.data.stream.lib import (
    _repeat,
    _iterate,
    _unfold,
    _head,
    _tail,
    _nth,
    _drop,
    _take,
    _prepend,
    _zipwith,
    _zip_stream,
    _interleave,
    _scanl,
    _tails,
    _cycle_sequence,
    _repeat_last,
    _prefix,
)
from typeclass.interpret.interpreter import evaluated

repeat         = evaluated(_repeat)
iterate        = evaluated(_iterate)
unfold         = evaluated(_unfold)
head           = evaluated(_head)
tail           = evaluated(_tail)
nth            = evaluated(_nth)
drop           = evaluated(_drop)
take           = evaluated(_take)
prepend        = evaluated(_prepend)
zipwith        = evaluated(_zipwith)
zip_stream     = evaluated(_zip_stream)
interleave     = evaluated(_interleave)
scanl          = evaluated(_scanl)
tails          = evaluated(_tails)
cycle_sequence = evaluated(_cycle_sequence)
repeat_last    = evaluated(_repeat_last)
prefix         = evaluated(_prefix)

