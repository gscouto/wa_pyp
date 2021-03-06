import matplotlib.pyplot as plt
import numpy as np
from astropy.io import fits
import os, sys
import time
import multiprocessing as mp
import matplotlib.gridspec as gridspec
from matplotlib.colorbar import Colorbar
import vorbin
from vorbin.voronoi_2d_binning import voronoi_2d_binning
from astropy.wcs import WCS

blue_cube = fits.open('/work1/gcouto/weave/datacubes/IFU_APERTIF_TEST/stackcube_1002022.fit')
red_cube = fits.open('/work1/gcouto/weave/datacubes/IFU_APERTIF_TEST/stackcube_1002021.fit')
aps_cube = fits.open('/work1/gcouto/weave/cube_creator/stackcube_1002022__stackcube_1002021__P001_APS_cube.fits')

gal_dir = 'galaxy_name/'
os.makedirs(gal_dir, exist_ok=True)

targetSN = 30
levels = np.array([3.,30.]) # SNR levels to display

colap_b_map = np.sum(blue_cube[1].data[:],axis=0)
colap_r_map = np.sum(red_cube[1].data[:],axis=0)
colap_a_map = np.sum(aps_cube[0].data[:],axis=0)

lam_r = red_cube[1].header['CRVAL3']+(np.arange(red_cube[1].header['NAXIS3'])*red_cube[1].header['CD3_3'])
lam_b = blue_cube[1].header['CRVAL3']+(np.arange(blue_cube[1].header['NAXIS3'])*blue_cube[1].header['CD3_3'])
lam_a = aps_cube[0].header['CRVAL3']+(np.arange(aps_cube[0].header['NAXIS3'])*aps_cube[0].header['CDELT3'])

sgn_b = np.mean(blue_cube[1].data[np.where(lam_b == 5100.)[0][0]-50:np.where(lam_b == 5100.)[0][0]+50], axis=0)
rms_b = np.std(blue_cube[1].data[np.where(lam_b == 5100.)[0][0]-50:np.where(lam_b == 5100.)[0][0]+50], axis=0)
snr_b = sgn_b / rms_b

sgn_r = np.mean(red_cube[1].data[np.where(lam_r == 6200.)[0][0]-50:np.where(lam_r == 6200.)[0][0]+50], axis=0)
rms_r = np.std(red_cube[1].data[np.where(lam_r == 6200.)[0][0]-50:np.where(lam_r == 6200.)[0][0]+50], axis=0)
snr_r = sgn_r / rms_r

sgn_a = np.mean(aps_cube[0].data[np.where(lam_a == min(lam_a, key=lambda x:abs(x-6200)))[0][0]-50:np.where(lam_a == min(lam_a, key=lambda x:abs(x-6200)))[0][0]+50], axis=0)
rms_a = np.std(aps_cube[0].data[np.where(lam_a == min(lam_a, key=lambda x:abs(x-6200)))[0][0]-50:np.where(lam_a == min(lam_a, key=lambda x:abs(x-6200)))[0][0]+50], axis=0)
snr_a = sgn_a / rms_a

# doing the plots

axis_header = fits.Header()
axis_header['NAXIS1'] = blue_cube[1].header['NAXIS1']
axis_header['NAXIS2'] = blue_cube[1].header['NAXIS2']
axis_header['CD1_1'] = blue_cube[1].header['CD1_1']
axis_header['CD2_2'] = blue_cube[1].header['CD2_2']
axis_header['CRPIX1'] = blue_cube[1].header['CRPIX1']
axis_header['CRPIX2'] = blue_cube[1].header['CRPIX2']
axis_header['CRVAL1'] = blue_cube[1].header['CRVAL1']
axis_header['CRVAL2'] = blue_cube[1].header['CRVAL2']
axis_header['CTYPE1'] = blue_cube[1].header['CTYPE1']
axis_header['CTYPE2'] = blue_cube[1].header['CTYPE2']
axis_header['CUNIT1'] = blue_cube[1].header['CUNIT1']
axis_header['CUNIT2'] = blue_cube[1].header['CUNIT2']

fig = plt.figure(figsize=(22,30))

gs = gridspec.GridSpec(6,8, height_ratios=[1,0.6,1,0.6,1,0.6], width_ratios=[1,0.06,0.3,1,0.06,0.3,1,0.06])
gs.update(left=0.07, right=0.9, bottom=0.05, top=0.95, wspace=0.0, hspace=0.25)
props = dict(boxstyle='round', facecolor='wheat', alpha=0.5)

fig.suptitle(blue_cube[0].header['CCNAME1']+' - '+blue_cube[0].header['PLATE']+' - '+blue_cube[0].header['MODE'], size=20)

wcs = WCS(axis_header)
ax = plt.subplot(gs[0,0], projection=wcs)

im = ax.imshow(np.arcsinh(colap_b_map), origin='lower')

ypmax_b = np.where(colap_b_map == np.nanmax(colap_b_map))[0]
xpmax_b = np.where(colap_b_map == np.nanmax(colap_b_map))[1]

ax.plot(xpmax_b,ypmax_b,'x',color='red',markersize=4,label=str(xpmax_b)+', '+str(ypmax_b))
ax.set_title('Collapsed Blue Arm Datacube')
ax.set_xlabel('Right Ascension (J2000)')
ax.set_ylabel('Declination (J2000)')
ax.legend()

cbax = plt.subplot(gs[0,1])
cbar = Colorbar(ax = cbax, mappable = im)
cbar.set_label('arcsinh scale')

ax = plt.subplot(gs[0,3])
im = ax.imshow(np.arcsinh(colap_r_map), origin='lower')

ypmax_r = np.where(colap_r_map == np.nanmax(colap_r_map))[0]
xpmax_r = np.where(colap_r_map == np.nanmax(colap_r_map))[1]

ax.plot(xpmax_r,ypmax_r,'x',color='red',markersize=4,label=str(xpmax_r)+', '+str(ypmax_r))
ax.set_title('Collapsed Red Arm Datacube')
ax.set_xlabel('X [px]')
ax.set_ylabel('Y [px]')
ax.legend()

cbax = plt.subplot(gs[0,4])
cbar = Colorbar(ax = cbax, mappable = im)
cbar.set_label('arcsinh scale')

ax = plt.subplot(gs[0,6])
im = ax.imshow(np.arcsinh(colap_a_map), origin='lower')

ypmax_a = np.where(colap_a_map == np.nanmax(colap_a_map))[0]
xpmax_a = np.where(colap_a_map == np.nanmax(colap_a_map))[1]

ax.plot(xpmax_a,ypmax_a,'x',color='red',markersize=4,label=str(xpmax_a)+', '+str(ypmax_a))
ax.set_title('Collapsed APS Datacube')
ax.set_xlabel('X [px]')
ax.set_ylabel('Y [px]')
ax.legend()

cbax = plt.subplot(gs[0,7])
cbar = Colorbar(ax = cbax, mappable = im)
cbar.set_label('arcsinh scale')

#------

ax = plt.subplot(gs[1,0])
ax.plot(lam_b,blue_cube[1].data[:,ypmax_b[0],xpmax_b[0]])
ax.set_xlabel(r'$\lambda$ [$\AA$]')
ax.set_ylabel('Flux?')
ax.set_title('Blue spectrum at ('+str(xpmax_b[0])+', '+str(ypmax_b[0])+')')

ax = plt.subplot(gs[1,3])
ax.plot(lam_r,red_cube[1].data[:,ypmax_r[0],xpmax_r[0]])
ax.set_xlabel(r'$\lambda$ [$\AA$]')
ax.set_ylabel('Flux?')
ax.set_title('Red spectrum at ('+str(xpmax_r[0])+', '+str(ypmax_r[0])+')')

ax = plt.subplot(gs[1,6])
ax.plot(lam_a,aps_cube[0].data[:,ypmax_a[0],xpmax_a[0]])
ax.set_xlabel(r'$\lambda$ [$\AA$]')
ax.set_ylabel('Flux?')
ax.set_title('APS spectrum at ('+str(xpmax_a[0])+', '+str(ypmax_a[0])+')')

#------

ax = plt.subplot(gs[2,0])
im = ax.imshow(snr_b, origin='lower')
cs = ax.contour(snr_b, levels,linestyles=np.array([':','-']), colors='white')
cs.collections[0].set_label('SNR = 3')
cs.collections[1].set_label('SNR = 30')
leg = ax.legend(framealpha=1,fontsize=8,loc='lower left')
leg.legendHandles[0].set_color('black')
leg.legendHandles[1].set_color('black')

ax.set_title(r'SNR @5100$\AA$')
ax.set_xlabel('X [px]')
ax.set_ylabel('Y [px]')

ims_xlims = ax.get_xlim()
ims_ylims = ax.get_ylim()

cbax = plt.subplot(gs[2,1])
cbar = Colorbar(ax = cbax, mappable = im)
cbar.set_label('SNR')

ax = plt.subplot(gs[2,3])
im = ax.imshow(snr_r, origin='lower')
cs = ax.contour(snr_r, levels,linestyles=np.array([':','-']), colors='white')
cs.collections[0].set_label('SNR = 3')
cs.collections[1].set_label('SNR = 30')
leg = ax.legend(framealpha=1,fontsize=8,loc='lower left')
leg.legendHandles[0].set_color('black')
leg.legendHandles[1].set_color('black')

ax.set_title(r'SNR @6200$\AA$')
ax.set_xlabel('X [px]')
ax.set_ylabel('Y [px]')

cbax = plt.subplot(gs[2,4])
cbar = Colorbar(ax = cbax, mappable = im)
cbar.set_label('SNR')

ax = plt.subplot(gs[2,6])
im = ax.imshow(snr_a, origin='lower')
cs = ax.contour(snr_a, levels,linestyles=np.array([':','-']), colors='white')
cs.collections[0].set_label('SNR = 3')
cs.collections[1].set_label('SNR = 30')
leg = ax.legend(framealpha=1,fontsize=8,loc='lower left')
leg.legendHandles[0].set_color('black')
leg.legendHandles[1].set_color('black')

ax.set_title(r'SNR @6200$\AA$')
ax.set_xlabel('X [px]')
ax.set_ylabel('Y [px]')

cbax = plt.subplot(gs[2,7])
cbar = Colorbar(ax = cbax, mappable = im)
cbar.set_label('SNR')

#------

ax = plt.subplot(gs[3,0])
ax.hist(snr_b[snr_b >= 3],30,histtype='step',lw=2)
ax.set_yscale('log')
ax.set_ylabel(r'N pixels [SNR $\geq$ 3]')
ax.set_xlabel(r'SNR [@5100$\AA$]')

int_spec_b = np.sum(blue_cube[1].data*((snr_b>=3)[np.newaxis,:,:]),axis=(1,2))
in_ax = ax.inset_axes([0.55,0.6,0.4,0.3])
in_ax.set_title(r'          integrated spec [SNR$\geq$3]',fontsize=10)
in_ax.plot(lam_b,int_spec_b)
in_ax.axvline(5050,linestyle='--',color='black')
in_ax.axvline(5150,linestyle='--',color='black')

ax = plt.subplot(gs[3,3])
ax.hist(snr_r[snr_r >= 3],30,histtype='step',lw=2)
ax.set_yscale('log')
ax.set_ylabel(r'N pixels [SNR $\geq$ 3]')
ax.set_xlabel(r'SNR [@6200$\AA$]')

int_spec_r = np.sum(red_cube[1].data*((snr_r>=3)[np.newaxis,:,:]),axis=(1,2))
in_ax = ax.inset_axes([0.55,0.6,0.4,0.3])
in_ax.set_title(r'          integrated spec [SNR$\geq$3]',fontsize=10)
in_ax.plot(lam_r,int_spec_r)
in_ax.axvline(6150,linestyle='--',color='black')
in_ax.axvline(6250,linestyle='--',color='black')

ax = plt.subplot(gs[3,6])
ax.hist(snr_a[snr_a >= 3],30,histtype='step',lw=2)
ax.set_yscale('log')
ax.set_ylabel(r'N pixels [SNR $\geq$ 3]')
ax.set_xlabel(r'SNR [@6200$\AA$]')

int_spec_a = np.sum(aps_cube[0].data*((snr_a>=3)[np.newaxis,:,:]),axis=(1,2))
in_ax = ax.inset_axes([0.55,0.6,0.4,0.3])
in_ax.set_title(r'          integrated spec [SNR$\geq$3]',fontsize=10)
in_ax.plot(lam_a,int_spec_a)
in_ax.axvline(6150,linestyle='--',color='black')
in_ax.axvline(6250,linestyle='--',color='black')

# doing voronoi binning

pixelsize = 1

yy, xx = np.indices(snr_r.shape)
yy_a, xx_a = np.indices(snr_a.shape)

x_t = np.ravel(xx)
y_t = np.ravel(yy)
x_ta = np.ravel(xx_a)
y_ta = np.ravel(yy_a)

sgn_t_r = np.ravel(sgn_r)
sgn_t_b = np.ravel(sgn_b)
sgn_t_a = np.ravel(sgn_a)
rms_t_r = np.ravel(rms_r)
rms_t_b = np.ravel(rms_b)
rms_t_a = np.ravel(rms_a)

x_t_b = x_t[sgn_t_b/rms_t_b > 3]
y_t_b = y_t[sgn_t_b/rms_t_b > 3]
sgn_tt_b = sgn_t_b[sgn_t_b/rms_t_b > 3]
rms_tt_b = rms_t_b[sgn_t_b/rms_t_b > 3]

binNum, xNode, yNode, xBar, yBar, sn, nPixels, scale = voronoi_2d_binning(x_t_b, y_t_b, sgn_tt_b, rms_tt_b, targetSN,pixelsize=pixelsize, plot=0, quiet=1)

ax = plt.subplot(gs[4,0])

xmin, xmax = np.min(x_t_b), np.max(x_t_b)
ymin, ymax = np.min(y_t_b), np.max(y_t_b)
nx = int(round((xmax - xmin)/pixelsize) + 1)
ny = int(round((ymax - ymin)/pixelsize) + 1)
img = np.full((nx, ny), np.nan)  # use nan for missing data
j = np.round((x_t_b - xmin)/pixelsize).astype(int)
k = np.round((y_t_b - ymin)/pixelsize).astype(int)
img[j, k] = binNum

rnd = np.argsort(np.random.random(xNode.size))  # Randomize bin colors
for i in np.arange(len(rnd)):
        img[img == np.unique(img)[i]] = rnd[i]

ax.imshow(np.rot90(img), interpolation='nearest', cmap='prism',
            extent=[xmin - pixelsize/2, xmax + pixelsize/2,
                    ymin - pixelsize/2, ymax + pixelsize/2])
ax.plot(xNode, yNode, '+w', scalex=False, scaley=False) # do not rescale after imshow()
ax.set_xlabel('X [px]')
ax.set_ylabel('Y [px]')
ax.set_xlim(ims_xlims)
ax.set_ylim(ims_ylims)
ax.imshow(snr_b*0.,zorder=-1,cmap='Greys',  interpolation='nearest')
ax.set_title(r'Voronoi binning / Target SNR = '+str(targetSN))

ax = plt.subplot(gs[5,0])

rad = np.sqrt((xBar-xpmax_b[0])**2 + (yBar-ypmax_b[0])**2)  # Use centroids, NOT generators
plt.plot(np.sqrt((x_t_b-xpmax_b[0])**2 + (y_t_b-ypmax_b[0])**2), sgn_tt_b/rms_tt_b, ',k')
plt.plot(rad[nPixels < 2], sn[nPixels < 2], 'xb', label='Not binned')
plt.plot(rad[nPixels > 1], sn[nPixels > 1], 'or', label='Voronoi bins')
plt.xlabel('R [pixels]')
plt.ylabel('Bin S/N')
plt.axis([np.min(rad), np.max(rad), 0, np.max(sn)*1.05])  # x0, x1, y0, y1
plt.axhline(targetSN)
plt.legend()

fits.writeto(gal_dir+'vorbin_map_blue.fits', np.flip(np.rot90(img),axis=0), overwrite=True)


x_t_r = x_t[sgn_t_r/rms_t_r > 3]
y_t_r = y_t[sgn_t_r/rms_t_r > 3]
sgn_tt_r = sgn_t_r[sgn_t_r/rms_t_r > 3]
rms_tt_r = rms_t_r[sgn_t_r/rms_t_r > 3]

binNum, xNode, yNode, xBar, yBar, sn, nPixels, scale = voronoi_2d_binning(x_t_r, y_t_r, sgn_tt_r, rms_tt_r, targetSN,pixelsize=pixelsize, plot=0, quiet=1)

ax = plt.subplot(gs[4,3])

xmin, xmax = np.min(x_t_r), np.max(x_t_r)
ymin, ymax = np.min(y_t_r), np.max(y_t_r)
nx = int(round((xmax - xmin)/pixelsize) + 1)
ny = int(round((ymax - ymin)/pixelsize) + 1)
img = np.full((nx, ny), np.nan)  # use nan for missing data
j = np.round((x_t_r - xmin)/pixelsize).astype(int)
k = np.round((y_t_r - ymin)/pixelsize).astype(int)
img[j, k] = binNum

rnd = np.argsort(np.random.random(xNode.size))  # Randomize bin colors
for i in np.arange(len(rnd)):
        img[img == np.unique(img)[i]] = rnd[i]
        
ax.imshow(np.rot90(img), interpolation='nearest', cmap='prism',
            extent=[xmin - pixelsize/2, xmax + pixelsize/2,
                    ymin - pixelsize/2, ymax + pixelsize/2])
ax.plot(xNode, yNode, '+w', scalex=False, scaley=False) # do not rescale after imshow()
ax.set_xlabel('X [px]')
ax.set_ylabel('Y [px]')
ax.set_xlim(ims_xlims)
ax.set_ylim(ims_ylims)
ax.imshow(snr_r*0.,zorder=-1,cmap='Greys',  interpolation='nearest')
ax.set_title(r'Voronoi binning / Target SNR = '+str(targetSN))

ax = plt.subplot(gs[5,3])

rad = np.sqrt((xBar-xpmax_r[0])**2 + (yBar-ypmax_r[0])**2)  # Use centroids, NOT generators
plt.plot(np.sqrt((x_t_b-xpmax_r[0])**2 + (y_t_b-ypmax_r[0])**2), sgn_tt_b/rms_tt_b, ',k')
plt.plot(rad[nPixels < 2], sn[nPixels < 2], 'xb', label='Not binned')
plt.plot(rad[nPixels > 1], sn[nPixels > 1], 'or', label='Voronoi bins')
plt.xlabel('R [pixels]')
plt.ylabel('Bin S/N')
plt.axis([np.min(rad), np.max(rad), 0, np.max(sn)*1.05])  # x0, x1, y0, y1
plt.axhline(targetSN)
plt.legend()

fits.writeto(gal_dir+'vorbin_map_red.fits', np.flip(np.rot90(img),axis=0), overwrite=True)


x_t_a = x_ta[sgn_t_a/rms_t_a > 3]
y_t_a = y_ta[sgn_t_a/rms_t_a > 3]
sgn_tt_a = sgn_t_a[sgn_t_a/rms_t_a > 3]
rms_tt_a = rms_t_a[sgn_t_a/rms_t_a > 3]

binNum, xNode, yNode, xBar, yBar, sn, nPixels, scale = voronoi_2d_binning(x_t_a, y_t_a, sgn_tt_a, rms_tt_a, targetSN,pixelsize=pixelsize, plot=0, quiet=1)

ax = plt.subplot(gs[4,6])

xmin, xmax = np.min(x_t_a), np.max(x_t_a)
ymin, ymax = np.min(y_t_a), np.max(y_t_a)
nx = int(round((xmax - xmin)/pixelsize) + 1)
ny = int(round((ymax - ymin)/pixelsize) + 1)
img = np.full((nx, ny), np.nan)  # use nan for missing data
j = np.round((x_t_a - xmin)/pixelsize).astype(int)
k = np.round((y_t_a - ymin)/pixelsize).astype(int)
img[j, k] = binNum

rnd = np.argsort(np.random.random(xNode.size))  # Randomize bin colors
for i in np.arange(len(rnd)):
        img[img == np.unique(img)[i]] = rnd[i]

ax.imshow(np.rot90(img), interpolation='nearest', cmap='prism',
            extent=[xmin - pixelsize/2, xmax + pixelsize/2,
                    ymin - pixelsize/2, ymax + pixelsize/2])
ax.plot(xNode, yNode, '+w', scalex=False, scaley=False) # do not rescale after imshow()
ax.set_xlabel('X [px]')
ax.set_ylabel('Y [px]')
ax.set_title(r'Voronoi binning / Target SNR = '+str(targetSN))

fits.writeto(gal_dir+'vorbin_map_aps.fits', np.flip(np.rot90(img),axis=0), overwrite=True)


ax = plt.subplot(gs[5,6])

rad = np.sqrt((xBar-xpmax_a[0])**2 + (yBar-ypmax_a[0])**2)  # Use centroids, NOT generators
plt.plot(np.sqrt((x_t_a-xpmax_a[0])**2 + (y_t_a-ypmax_a[0])**2), sgn_tt_a/rms_tt_a, ',k')
plt.plot(rad[nPixels < 2], sn[nPixels < 2], 'xb', label='Not binned')
plt.plot(rad[nPixels > 1], sn[nPixels > 1], 'or', label='Voronoi bins')
plt.xlabel('R [pixels]')
plt.ylabel('Bin S/N')
plt.axis([np.min(rad), np.max(rad), 0, np.max(sn)*1.05])  # x0, x1, y0, y1
plt.axhline(targetSN)
plt.legend()

plt.savefig(gal_dir+'QC_plots.pdf')
