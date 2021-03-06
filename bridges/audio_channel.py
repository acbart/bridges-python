##
#  @brief This is a class in BRIDGES a channel of audio data
#
#  This class contains one channel of 8, 16, 24, or 32 bit audio samples.
#
#  @author Luke Sloop
#
#  @date 2020, 1/31/2020
#
class AudioChannel(object):
    def __init__(self, sample_count: int=0, sample_bits: int=32) -> None:
        """
            AudioChannel constructor
            args:
                (int) sample_count: The total number of samples in this audio channel
            Returns:
                None
        """
        self.__data = [0 for _ in range(sample_count)]
        self._sample_count = sample_count
        self._sample_bits = 32

    def set_sample(self, index: int, value: int) -> None:
        """
            Set the sample at index. The sample value should be a valid signed integer with get_sample_bits() number of bits.
            args:
                (int) index: The index on this channel to set
                (int) value: The signed integer value to set the sample to
            Returns:
                None
        """
        minmax = (2 ** self.get_sample_bits() // 2) - 1
        if value < -minmax - 1:
            raise ValueError("Sample value out of minimum for signed %d bit integer with value %d" % (self.get_sample_bits(), value))
        if value > minmax:
            raise ValueError("Sample value out of maxmium for signed %d bit integer with value %d" % (self.get_sample_bits(), value))

        self.__data[index] = value

    def get_sample(self, index: int) -> int:
        """
            Get the sample at index. The sample will be a signed integer with get_sample_bits() number of bits.
            args:
                (int) index: The sample index on this channel to get
            Returns:
                int: The sample at index that is an integer within the range of an integer of get_sample_bits() number of bits.
        """
        return self.__data[index]

    def get_sample_count(self) -> int:
        """
            Get the number of samples or length of this channel.
            Returns:
                int: The number of samples in this channel.
        """
        return self._sample_count

    def get_sample_bits(self) -> int:
        """
            Get the number of bits that make the samples in this channel.
            Will be 8, 16, 24, or 32.
            Returns:
                int: The number of bits that make the samples in this channel.
        """
        return self._sample_bits