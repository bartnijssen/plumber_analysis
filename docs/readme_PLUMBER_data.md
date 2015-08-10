# Data problems with PLUMBER data

## Time axis

There is a lot of inconsistency between the time axes used by the different models. This complicates analysis with packages (such as python's pandas) that can actually use the time stamp to do sophisticated time series analysis. All of these problems can be managed by simply using the index (except for CHTESSEL, which has multiple problems), but this should be resolved by replacing the time axis with the correct values.

### Extent of period covered
Four sites have record lengths that are inconsistent with [Table 1 in Best et al. 2015](http://journals.ametsoc.org/action/showFullPopup?doi=10.1175%2FJHM-D-14-0158.1&id=_i6).

|Location | Period in data files | Period in [Table 1](http://journals.ametsoc.org/action/showFullPopup?doi=10.1175%2FJHM-D-14-0158.1&id=_i6)|
|:-------------|-------------:|-----:|
|Bugac        | 2003 2006 | 2002 2006|
|ElSaler      | 1999 2006 | 2003 2006|
|Espirra      | 2002 2005 | 2001 2006|
|Hesse        | 2001 2006 | 1999 2006|

### Averaging period
 * CHTESSEL appears to have a timestamp that denotes the beginning of the time step (precedes other models by 30 minutes). However, this is not entirely clear, because CHTESSEL also includes one extra time step per year compared to all the other models.
 * COLASSiB.2.0 has a timestamp that is delayed by 30 minutes compared to the other models. This just seems to be an error.
 * ORCHIDEE.trunk_r1402 uses time bounds to denote the interval over which the value is valid. While this may be the most correct way of providing time information, it requires additional handling of the time axis, which is probably not necessary.

### Time intervals
A number of models have irregular time intervals, which is probably unintended. For example, most models have regular intervals of 1800 seconds most of the time, but this changes to timesteps of different length for some of the sites that have long records. It is not clear whether this stems for a problem with using `float`  to denote the time axis, since the same happens for some models that use `double`. It is likely that this originated in some intermediate processing steps.

For example, CABLE.2.0 and CABLE_2.0_SLI.vxh599_r553 consistently start having irregular time intervals from record 74566 onwards, e.g. `CABLE.2.0_HesseFluxnet.1.4.nc`
```
time[74560]=134209800 seconds since 2001-01-01 00:00:00
time[74561]=134211600 seconds since 2001-01-01 00:00:00
time[74562]=134213400 seconds since 2001-01-01 00:00:00
time[74563]=134215200 seconds since 2001-01-01 00:00:00
time[74564]=134217000 seconds since 2001-01-01 00:00:00
time[74565]=134218800 seconds since 2001-01-01 00:00:00
time[74566]=134220608 seconds since 2001-01-01 00:00:00
time[74567]=134222400 seconds since 2001-01-01 00:00:00
time[74568]=134224192 seconds since 2001-01-01 00:00:00
time[74569]=134226000 seconds since 2001-01-01 00:00:00
```

when converting these time stamps, they become
```
2005-04-03 08:30:00
2005-04-03 09:00:00
2005-04-03 09:30:00
2005-04-03 10:00:00
2005-04-03 10:30:00
2005-04-03 11:00:00
2005-04-03 11:30:08
2005-04-03 12:00:00
2005-04-03 12:29:52
2005-04-03 13:00:00
```

The following sites and models are problematic (the number is the number of intervals (lag-1) that are not equal to 1800s)

```
Site: Amplero          -- LSM: CHTESSEL                  :  32801
Site: Blodgett         -- LSM: CABLE.2.0                 :  48170
Site: Blodgett         -- LSM: CABLE_2.0_SLI.vxh599_r553 :  48170
Site: Blodgett         -- LSM: CHTESSEL                  :  85412
Site: Blodgett         -- LSM: COLASSiB.2.0              :  48170
Site: Blodgett         -- LSM: JULES.3.1                 :  48169
Site: Blodgett         -- LSM: JULES3.1_altP             :  48169
Site: Bugac            -- LSM: CHTESSEL                  :  32801
Site: ElSaler          -- LSM: CABLE.2.0                 :  65690
Site: ElSaler          -- LSM: CABLE_2.0_SLI.vxh599_r553 :  65690
Site: ElSaler          -- LSM: CHTESSEL                  : 102933
Site: ElSaler          -- LSM: COLASSiB.2.0              :  65690
Site: ElSaler          -- LSM: JULES.3.1                 :  65689
Site: ElSaler          -- LSM: JULES3.1_altP             :  65689
Site: ElSaler2         -- LSM: CHTESSEL                  :      1
Site: Espirra          -- LSM: CHTESSEL                  :  32801
Site: FortPeck         -- LSM: CABLE.2.0                 :  48170
Site: FortPeck         -- LSM: CABLE_2.0_SLI.vxh599_r553 :  48170
Site: FortPeck         -- LSM: CHTESSEL                  :  85412
Site: FortPeck         -- LSM: COLASSiB.2.0              :  48170
Site: FortPeck         -- LSM: JULES.3.1                 :  48169
Site: FortPeck         -- LSM: JULES3.1_altP             :  48169
Site: Harvard          -- LSM: CABLE.2.0                 :  65690
Site: Harvard          -- LSM: CABLE_2.0_SLI.vxh599_r553 :  65690
Site: Harvard          -- LSM: CHTESSEL                  : 102933
Site: Harvard          -- LSM: COLASSiB.2.0              :  65690
Site: Harvard          -- LSM: JULES.3.1                 :  65689
Site: Harvard          -- LSM: JULES3.1_altP             :  65689
Site: Hesse            -- LSM: CABLE.2.0                 :  30602
Site: Hesse            -- LSM: CABLE_2.0_SLI.vxh599_r553 :  30602
Site: Hesse            -- LSM: CHTESSEL                  :  67843
Site: Hesse            -- LSM: COLASSiB.2.0              :  30602
Site: Hesse            -- LSM: JULES.3.1                 :  30601
Site: Hesse            -- LSM: JULES3.1_altP             :  30601
Site: Howard           -- LSM: CHTESSEL                  :  32801
Site: Howlandm         -- LSM: CABLE.2.0                 :  83258
Site: Howlandm         -- LSM: CABLE_2.0_SLI.vxh599_r553 :  83258
Site: Howlandm         -- LSM: CHTESSEL                  : 120502
Site: Howlandm         -- LSM: COLASSiB.2.0              :  83258
Site: Howlandm         -- LSM: JULES.3.1                 :  83257
Site: Howlandm         -- LSM: JULES3.1_altP             :  83257
Site: Hyytiala         -- LSM: CHTESSEL                  :  32801
Site: Kruger           -- LSM: CHTESSEL                  :      1
Site: Loobos           -- LSM: CABLE.2.0                 : 100730
Site: Loobos           -- LSM: CABLE_2.0_SLI.vxh599_r553 : 100730
Site: Loobos           -- LSM: CHTESSEL                  : 137975
Site: Loobos           -- LSM: COLASSiB.2.0              : 100730
Site: Loobos           -- LSM: JULES.3.1                 : 100729
Site: Loobos           -- LSM: JULES3.1_altP             : 100729
Site: Merbleue         -- LSM: CABLE.2.0                 :  48170
Site: Merbleue         -- LSM: CABLE_2.0_SLI.vxh599_r553 :  48170
Site: Merbleue         -- LSM: CHTESSEL                  :  85412
Site: Merbleue         -- LSM: COLASSiB.2.0              :  48170
Site: Merbleue         -- LSM: JULES.3.1                 :  48169
Site: Merbleue         -- LSM: JULES3.1_altP             :  48169
Site: Mopane           -- LSM: CHTESSEL                  :  15280
Site: Palang           -- LSM: CHTESSEL                  :      1
Site: Sylvania         -- LSM: CHTESSEL                  :  32801
Site: Tumba            -- LSM: CHTESSEL                  :  32801
Site: UniMich          -- LSM: CABLE.2.0                 :  13082
Site: UniMich          -- LSM: CABLE_2.0_SLI.vxh599_r553 :  13082
Site: UniMich          -- LSM: CHTESSEL                  :  50322
Site: UniMich          -- LSM: COLASSiB.2.0              :  13082
Site: UniMich          -- LSM: JULES.3.1                 :  13081
Site: UniMich          -- LSM: JULES3.1_altP             :  13081
```

### Duplicate time steps
CHTESSEL includes duplicate timesteps for all sites. It appears to be the only model that does. Specifically the timestamps for the first timestep of the year are duplicated (perhaps from concatenating annual files), e.g. `CHTESSEL_UniMichFluxnet.1.4.nc`

```
1999-12-31 23:30:00
2000-01-01 00:00:00
2000-01-01 00:00:00
2000-01-01 00:30:00
...
2000-12-31 23:30:00
2001-01-01 00:00:00
2001-01-01 00:00:00
2001-01-01 00:30:00
...
2001-12-31 23:30:04
2001-12-31 23:59:56
2001-12-31 23:59:56
2002-01-01 00:30:04
...
2002-12-31 23:30:04
2002-12-31 23:59:56
2002-12-31 23:59:56
2003-01-01 00:30:04
```

Note however that the variable values are *NOT* identical for the duplicated timesteps at least not for all variables For example, in `CHTESSEL_UniMichFluxnet.1.4.nc`, the variable `LWnet` is identical for the duplicated time steps, while `Qh` and `Qle` are not. This makes it difficult to interpret the CHTESSEL record, e.g.
```
time			          LWnet	      Qh	        Qle
2002-12-31 23:30:04	-60.359535	-26.218668	-0.297246
2002-12-31 23:59:56	-51.313972	-27.488554	-0.360814
2002-12-31 23:59:56	-51.313972	-30.257700	-0.364292
2003-01-01 00:30:04	-48.550117	-30.730211	-0.326920
```

The following is a list by site of the number of duplicated time steps in CHTESSEL:
```
Site: Amplero          -- LSM: CHTESSEL                  :      3
Site: Blodgett         -- LSM: CHTESSEL                  :      6
Site: Bugac            -- LSM: CHTESSEL                  :      3
Site: ElSaler          -- LSM: CHTESSEL                  :      7
Site: ElSaler2         -- LSM: CHTESSEL                  :      1
Site: Espirra          -- LSM: CHTESSEL                  :      3
Site: FortPeck         -- LSM: CHTESSEL                  :      6
Site: Harvard          -- LSM: CHTESSEL                  :      7
Site: Hesse            -- LSM: CHTESSEL                  :      5
Site: Howard           -- LSM: CHTESSEL                  :      3
Site: Howlandm         -- LSM: CHTESSEL                  :      8
Site: Hyytiala         -- LSM: CHTESSEL                  :      3
Site: Kruger           -- LSM: CHTESSEL                  :      1
Site: Loobos           -- LSM: CHTESSEL                  :      9
Site: Merbleue         -- LSM: CHTESSEL                  :      6
Site: Mopane           -- LSM: CHTESSEL                  :      2
Site: Palang           -- LSM: CHTESSEL                  :      1
Site: Sylvania         -- LSM: CHTESSEL                  :      3
Site: Tumba            -- LSM: CHTESSEL                  :      3
Site: UniMich          -- LSM: CHTESSEL                  :      4
```

### Leap years
CHTESSEL appears to be the only model that does not include leap days given the number of timesteps in its files. Because it also has duplicate timesteps, the number of timesteps differs from the other models for the same site by a number other than 48 (number of half hours in a day). For example, for Amplero, the difference is 44 timesteps (70084 rather than 70128), because it includes 3 duplicate timesteps plus an extra timestep at the beginning or end of the file, while missing the leap day in 2004. As a result - strictly by decoding the timestep, the last day of the simulation (2006/12/31) is missing.

Since there is no calendar information in the meta data (e.g. `Calendar : NO_LEAP`) this cannot easily be handled programmatically.

## Sign convention

Both CHTESSEL and ISBA_SURFEX_3l.SURFEX7.3 have a global attribute

`SurfSgn_convention = "Mathematical"`

but CHTESSEL has fluxes that are of opposite sign to most other models. Clearly CHTESSEL and ISBA_SURFEX_3l.SURFEX7.3 cannot both be correct in their `SurfSgn_convention`. Unfortunately this prevents scripts that use these files from programmatically standardizing on a sign convention.

## Site characteristics

### location
The latitude and longitude variables that are in most of the files (but not all), are not consistent.

* Three of the models have the same coordinates for all sites: `Mosaic.1`, `NOAH.2.7.1`, and `NOAH.3.3` have (latitude, longitude) pairs of (-35.65570,  148.15199) for all sites.

* The models `CABLE.2.0`, `CABLE_2.0_SLI.vxh599_r553`, `Manabe_Bucket.2`, and `Penman_Monteith.1` have the same coordinates (which - as expected - vary by site), but they are slightly different from the coordinates used by the other models and the meteorological and flux observations. For example, for Amplero, these sites have (latitude, longitude) equal to (38.94780, -120.76991), while the other models have (38.89520, -120.63300).

* Some models have a different organization and name for the latitude and longitude variable. For example, for `ORCHIDEE_.trunk_r1401`, longitude is organized as `float lon(lon)`, whereas for many other files it is `float longitude(y, x)` (e.g. `CABLE_2.0`). This makes it difficult to handle the coordinates programmatically.

## Data problems

Some of the models show erratic behavior for some of the locations. For example, ORCHIDEE.trunk_r1401 has a rapidly varying `Qle` flux on some days in the middle of January 2002 at Palang (note that the time record in the following has been made consistent with the other models and that `Rnet` is simply the sum of `SWnet` and `LWnet`):

```
time                SWnet	    LWnet	      Qh          Qle       Rnet
2002-01-15 00:30:00	0.000000	-28.242348	-12.058269	4.310206	-28.242348
2002-01-15 01:00:00	0.000000	-27.968828	-5.886511	3.025634	-27.968828
2002-01-15 01:30:00	0.000000	-27.578209	-0.790448	0.220864	-27.578209
2002-01-15 02:00:00	0.000000	-26.885384	-1.390682	-0.168012	-26.885384
2002-01-15 02:30:00	0.000000	-26.581457	-2.394639	-0.609286	-26.581457
2002-01-15 03:00:00	0.000000	-26.724857	-2.291152	-0.407377	-26.724857
2002-01-15 03:30:00	0.000000	-26.835474	-2.107383	-0.259738	-26.835474
2002-01-15 04:00:00	0.000000	-25.813187	-0.298009	-0.076463	-25.813187
2002-01-15 04:30:00	0.000000	-24.981293	-0.159859	-0.064694	-24.981293
2002-01-15 05:00:00	0.000000	-24.779198	-0.161559	-0.072854	-24.779198
2002-01-15 05:30:00	0.000000	-24.685720	-0.458561	-0.226937	-24.685720
2002-01-15 06:00:00	2.826812	-25.301706	-1.596866	-0.964218	-22.474895
2002-01-15 06:30:00	5.653623	-26.616131	-3.571213	-2.611705	-20.962508
2002-01-15 07:00:00	22.647339	-28.562962	-2.266110	-3.290418	-5.915623
2002-01-15 07:30:00	39.641052	-31.469028	1.680270	-3.245759	8.172024
2002-01-15 08:00:00	40.087738	-31.358719	5.035008	3.443952	8.729019
2002-01-15 08:30:00	40.534420	-30.838816	4.451329	5.486068	9.695604
2002-01-15 09:00:00	58.592297	-32.477757	14.027551	13.268847	26.114540
2002-01-15 09:30:00	76.650169	-33.844616	20.493279	23.426098	42.805553
2002-01-15 10:00:00	292.343994	-66.216515	25.317221	7.767337	226.127480
2002-01-15 10:30:00	508.037842	-35.279358	25.471083	567.050659	472.758484
2002-01-15 11:00:00	568.077454	-113.402206	9.514337	4.542570	454.675247
2002-01-15 11:30:00	628.117126	-16.177387	-374.765167	1388.269043	611.939739
2002-01-15 12:00:00	569.478882	-106.906822	1.216020	0.247543	462.572060
2002-01-15 12:30:00	510.840576	-36.085785	-192.070175	956.841125	474.754791
2002-01-15 13:00:00	549.027710	-109.892769	13.764935	17.436483	439.134941
2002-01-15 13:30:00	587.214844	-47.057423	-120.179344	921.735840	540.157421
2002-01-15 14:00:00	633.000000	-109.778679	49.033604	75.423508	523.221321
2002-01-15 14:30:00	678.785156	-52.577148	-21.068316	875.025391	626.208008
2002-01-15 15:00:00	608.760803	-86.802788	92.030777	194.862015	521.958015
2002-01-15 15:30:00	538.736450	-60.190826	17.201464	561.349426	478.545624
2002-01-15 16:00:00	449.333893	-67.904411	39.670704	263.737152	381.429482
2002-01-15 16:30:00	359.931305	-60.737259	-16.937580	326.588226	299.194046
2002-01-15 17:00:00	271.579773	-76.230270	3.995879	44.575150	195.349503
2002-01-15 17:30:00	183.228195	-54.612610	-108.867531	330.220093	128.615585
2002-01-15 18:00:00	98.943665	-58.026615	-0.107798	5.110007	40.917049
2002-01-15 18:30:00	14.659131	-51.885483	-70.350975	62.517170	-37.226352
2002-01-15 19:00:00	7.329566	-43.843876	-6.140556	27.175095	-36.514310
2002-01-15 19:30:00	0.000000	-40.998623	-5.147423	0.593676	-40.998623
2002-01-15 20:00:00	0.000000	-38.873734	-12.850510	0.731340	-38.873734
2002-01-15 20:30:00	0.000000	-37.458626	-8.379104	0.682773	-37.458626
2002-01-15 21:00:00	0.000000	-37.676231	-7.865889	0.643172	-37.676231
2002-01-15 21:30:00	0.000000	-37.921932	-6.635191	0.612106	-37.921932
2002-01-15 22:00:00	0.000000	-36.920219	-7.078890	0.531829	-36.920219
2002-01-15 22:30:00	0.000000	-36.111134	-6.674271	0.472052	-36.111134
2002-01-15 23:00:00	0.000000	-35.013859	-4.993677	0.406031	-35.013859
2002-01-15 23:30:00	0.000000	-33.979572	-3.409106	0.345025	-33.979572
2002-01-16 00:00:00	0.000000	-32.945362	-2.758436	0.285288	-32.945362
2002-01-16 00:30:00	0.000000	-32.000389	-1.800277	0.233411	-32.000389
```

Note the strong oscillations in the model output (`Qle` in particular), for example, from `10:00 - 14:30`, `Qle` has the sequence `7.8 / 567 / 4.5 / 1388 / 0.2 / 957 / 17 / 922 / 75.4 / 875`. These oscillations are strong enough that they show as a sawtooth pattern in the mean diurnal cycle for this site.

The concern is that this pattern is not apparent in the net radiation and therefore it is not clear whether this is a data error or actual model output. If it is actual model output, then it is "fair game", but I would like to avoid basing the analysis on processing errors.
