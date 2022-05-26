


def NaNC(df):
    import numpy as np
    df.loc[df.isnull().any(axis=1), :] = np.nan
    return df

def interpolate_outliers(data_mat, boundaries):
    import numpy as np
    from scipy.interpolate import griddata
    N = data_mat.shape[1]
    timevec = np.arange(0,N)/N

    dat = list()
    for row in range(0, data_mat.shape[0]):
        temp_dat = data_mat[row]
        idnan = np.isnan(temp_dat)

        outliers = (temp_dat > boundaries['UPPER'][0][row]) | (temp_dat < boundaries["LOWER"][0][row])
        if np.sum(outliers) > 0:
            mask = (temp_dat > boundaries['UPPER'][0][row]) | (temp_dat < boundaries["LOWER"][0][row]) | (np.isnan(temp_dat))
            temp_dat[mask] = griddata(timevec[~mask], temp_dat[~mask], timevec[mask], method='cubic')
            temp_dat[idnan] = np.nan
            dat.append(temp_dat)
        else:
            dat.append(temp_dat)
    datAll = np.vstack(dat)
    return datAll
