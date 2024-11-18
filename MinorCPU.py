from m5.objects import *

class MinorDefaultFUPool(FUPool):
    def __init__(self, **kwargs):
        super(MinorDefaultFUPool, self).__init__(**kwargs)
        self.funcUnits = [
            # Existing functional units...

            # FloatSimdFU configurations with opLat + issueLat = 7
            MinorFU(
                opLat=1,
                issueLat=6,
                opClasses=minorMakeOpClassSet([...]),
                timings=[...],
                description="FloatSimdFU opLat=1 issueLat=6"
            ),
            MinorFU(
                opLat=2,
                issueLat=5,
                opClasses=minorMakeOpClassSet([...]),
                timings=[...],
                description="FloatSimdFU opLat=2 issueLat=5"
            ),
            # Additional configurations...

            # New configurations with opLat + issueLat = 8
            MinorFU(
                opLat=2,
                issueLat=6,
                opClasses=minorMakeOpClassSet([...]),
                timings=[...],
                description="FloatSimdFU opLat=2 issueLat=6"
            ),
            MinorFU(
                opLat=4,
                issueLat=4,
                opClasses=minorMakeOpClassSet([...]),
                timings=[...],
                description="FloatSimdFU opLat=4 issueLat=4"
            ),
            MinorFU(
                opLat=6,
                issueLat=2,
                opClasses=minorMakeOpClassSet([...]),
                timings=[...],
                description="FloatSimdFU opLat=6 issueLat=2"
            ),
            # Other functional units...
        ]
