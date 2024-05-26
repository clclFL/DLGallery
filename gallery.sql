use deeplearning_gallery;

insert into db_admin (username, `password`, email, permission, `status`, create_time)
values ('root', 'scrypt:32768:8:1$TmCTIEW0IKRjdXy8$7817961129f5b463d4aa0fcfa6a35c063d945944d31db3ad1da9481ad13c7c8589ae6d2da3b8dd3d637d1bf220b328b722a5a4da4192853525a3ed214767f321', 'pineclone@outlook.com', '0', '1', now());

insert into db_user (username, `password`, email, `status`, create_time)
values ('anonymous', 'scrypt:32768:8:1$TmCTIEW0IKRjdXy8$7817961129f5b463d4aa0fcfa6a35c063d945944d31db3ad1da9481ad13c7c8589ae6d2da3b8dd3d637d1bf220b328b722a5a4da4192853525a3ed214767f321', 'pineclone@outlook.com', '1', now());

insert into db_modelpanel
(title, banner, `inner`, `icon`, likes, `status`, create_time, admin_id, category, forward)
values ('ID Card Scanning', 'Easy way check card scanning', 'Using Cncor as a scanning solution',
'images/idcard-scanning-icon.jpg', 0, 1, now(), 1, 0, 'idscanner');