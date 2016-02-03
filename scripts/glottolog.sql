select distinct
  l.id,
  l.name,
  l.level,
  l.status,
  l.fid as family_id,
  l.fname as family_name,
  l.latitude,
  l.longitude,
  iso.name as iso_code
from
  (
    select
      l.pk,
      l.id,
      l.name,
      ll.level,
      ll.status,
      f.id as fid,
      f.name as fname,
      l.latitude,
      l.longitude
    from
      language as l,
      languoid as ll,
      language as f
    where
      l.pk = ll.pk and ll.family_pk = f.pk and l.active = TRUE 
  ) as l
left outer join
  (
    select
      i.name, li.language_pk
    from
      languageidentifier as li, identifier as i
    where
      li.identifier_pk = i.pk and i.type = 'iso639-3'
  ) as iso on (iso.language_pk = l.pk)
order by l.id;
