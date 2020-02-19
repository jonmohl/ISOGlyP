def basicEVP(seq, positions, dict):
   evp = 1;
   for n in range(0,5):
      if positions[n] == 1:
         evp = evp * dict[seq[n]][n]
   for n in range(6,len(positions)+1):
      if positions[n-1] == 1:
         evp = evp * dict[seq[n]][n-1]
   return evp

def preExtEVP(seq, positions, dict):
   evp = 1;
   for n in range(0,5):
      if positions[n] == 1:
         evp = evp * dict[seq[n]][n+1]
   for n in range(6,len(positions)+1):
      if positions[n-1] == 1:
         evp = evp * dict[seq[n]][n]
   return evp
